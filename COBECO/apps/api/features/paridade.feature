# language: pt
Funcionalidade: Agrupamento de fornecedores por paridade
  Como usuário do COBECO
  Quero agrupar fornecedores pelo conjunto idêntico de itens disponíveis
  Para comparar coberturas equivalentes

  Cenário: Agrupar oito fornecedores com quatro perfis de cobertura
    Dado uma lista com os produtos de 1 a 9
    E os fornecedores A a H com as coberturas especificadas
    Quando o motor calcular os grupos de paridade
    Então serão gerados 4 grupos
    E os grupos serão "A,B;C,E,F,H;D;G"
