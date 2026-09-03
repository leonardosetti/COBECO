-- RF01/RF02: a identidade do usuário passa a ter username único, e o login
-- aceita e-mail ou username.
ALTER TABLE "User" ADD COLUMN "username" TEXT;

-- Contas já existentes recebem um username derivado do e-mail. O sufixo
-- numérico resolve o caso de dois e-mails com o mesmo prefixo local.
UPDATE "User" AS u
SET "username" = derived."candidate"
FROM (
  SELECT
    "id",
    CASE
      WHEN row_number() OVER (PARTITION BY "base" ORDER BY "createdAt", "id") = 1 THEN "base"
      ELSE "base" || '_' || row_number() OVER (PARTITION BY "base" ORDER BY "createdAt", "id")
    END AS "candidate"
  FROM (
    SELECT
      "id",
      "createdAt",
      left(regexp_replace(lower(split_part("email", '@', 1)), '[^a-z0-9_]', '', 'g'), 24) AS "base"
    FROM "User"
  ) AS normalized
) AS derived
WHERE u."id" = derived."id";

-- Rede de segurança para e-mails cujo prefixo desaparece na normalização ou
-- fica abaixo do mínimo de 3 caracteres exigido pelo RF01.
UPDATE "User"
SET "username" = 'user_' || left(replace("id", '-', ''), 12)
WHERE "username" IS NULL OR length("username") < 3;

ALTER TABLE "User" ALTER COLUMN "username" SET NOT NULL;

CREATE UNIQUE INDEX "User_username_key" ON "User"("username");
CREATE INDEX "User_username_idx" ON "User"("username");
