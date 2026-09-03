-- RF09: a exclusão de lista passa a ser lógica, preservando o histórico de
-- cotações que aponta para ela.
ALTER TABLE "ProductList" ADD COLUMN "deletedAt" TIMESTAMP(3);

CREATE INDEX "ProductList_deletedAt_idx" ON "ProductList"("deletedAt");
