from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models.agendamento import Agendamento
from backend.models.cliente import Cliente
from backend.models.database import db

agendamento_bp = Blueprint("agendamento", __name__, url_prefix="/agendamentos")


@agendamento_bp.route("/", methods=["GET"])
def listar_agendamentos():
    """
    Retorna lista de agendamentos (todos ou filtrados por status/data)
    """
    status = request.args.get("status", default=None)
    data_inicio = request.args.get("data_inicio", default=None)
    query = Agendamento.query

    if status:
        query = query.filter_by(status=status)
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            query = query.filter(Agendamento.data >= data_inicio_dt)
        except ValueError:
            return jsonify({"error": "Data inválida"}), 400

    agendamentos = query.order_by(Agendamento.data, Agendamento.hora).all()

    resultado = []
    for ag in agendamentos:
        resultado.append({
            "id": ag.id,
            "cliente_id": ag.cliente_id,
            "cliente_nome": ag.cliente.nome if ag.cliente else None,
            "data": ag.data.strftime("%Y-%m-%d"),
            "hora": ag.hora.strftime("%H:%M"),
            "servicos": ag.servicos,
            "status": ag.status
        })

    return jsonify(resultado)


@agendamento_bp.route("/", methods=["POST"])
def criar_agendamento():
    """
    Cria novo agendamento, verificando conflito de horário.
    JSON esperado:
    {
        "cliente_id": int,
        "data": "YYYY-MM-DD",
        "hora": "HH:MM",
        "servicos": "string com serviços separados por vírgula"
    }
    """
    data = request.get_json()
    cliente_id = data.get("cliente_id")
    data_str = data.get("data")
    hora_str = data.get("hora")
    servicos = data.get("servicos")

    if not all([cliente_id, data_str, hora_str, servicos]):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    # Validar data e hora
    try:
        data_dt = datetime.strptime(data_str, "%Y-%m-%d").date()
        hora_dt = datetime.strptime(hora_str, "%H:%M").time()
    except ValueError:
        return jsonify({"error": "Data ou hora com formato inválido"}), 400

    # Verificar conflito: já existe agendamento no mesmo dia e hora?
    conflito = Agendamento.query.filter_by(data=data_dt, hora=hora_dt, status="Agendado").first()
    if conflito:
        return jsonify({"error": "Já existe um agendamento nesse dia e horário"}), 409

    # Verificar cliente existe
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    novo_agendamento = Agendamento(
        cliente_id=cliente_id,
        data=data_dt,
        hora=hora_dt,
        servicos=servicos,
        status="Agendado"
    )

    db.session.add(novo_agendamento)
    db.session.commit()

    return jsonify({"msg": "Agendamento criado com sucesso", "id": novo_agendamento.id}), 201


@agendamento_bp.route("/<int:id>", methods=["PUT"])
def reagendar(id):
    """
    Reagendar agendamento: atualizar data e hora.
    JSON esperado:
    {
        "data": "YYYY-MM-DD",
        "hora": "HH:MM"
    }
    """
    agendamento = Agendamento.query.get_or_404(id)
    data = request.get_json()

    data_str = data.get("data")
    hora_str = data.get("hora")
    if not all([data_str, hora_str]):
        return jsonify({"error": "Data e hora obrigatórios"}), 400

    try:
        data_dt = datetime.strptime(data_str, "%Y-%m-%d").date()
        hora_dt = datetime.strptime(hora_str, "%H:%M").time()
    except ValueError:
        return jsonify({"error": "Data ou hora inválida"}), 400

    # Verificar conflito de horário (exceto o próprio agendamento)
    conflito = Agendamento.query.filter(
        Agendamento.data == data_dt,
        Agendamento.hora == hora_dt,
        Agendamento.status == "Agendado",
        Agendamento.id != id
    ).first()
    if conflito:
        return jsonify({"error": "Já existe um agendamento nesse dia e horário"}), 409

    agendamento.data = data_dt
    agendamento.hora = hora_dt
    agendamento.status = "Reagendado"
    db.session.commit()

    return jsonify({"msg": "Agendamento reagendado com sucesso"})


@agendamento_bp.route("/<int:id>/cancelar", methods=["PUT"])
def cancelar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = "Cancelado"
    db.session.commit()
    return jsonify({"msg": "Agendamento cancelado com sucesso"})

