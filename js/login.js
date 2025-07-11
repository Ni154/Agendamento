<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Teste Supabase</title>
</head>
<body>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js"></script>

<script>
  const SUPABASE_URL = "https://stqbqsrznhhtbvjeugyb.supabase.co";
  const SUPABASE_KEY = "sb_publishable_XmW5t1y3YcJWzCYlvRtLDA_LcJSs4gH";

  const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

  (async () => {
    const { data, error } = await supabase
      .from("usuarios")
      .select("*")
      .eq("usuario", "admin")
      .eq("senha", "admin")
      .single();

    console.log("Dados:", data);
    console.log("Erro:", error);
  })();
</script>

</body>
</html>
