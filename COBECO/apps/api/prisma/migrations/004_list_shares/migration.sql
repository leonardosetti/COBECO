CREATE TABLE "ListShare" (
    "id" TEXT NOT NULL,
    "listId" TEXT NOT NULL,
    "token" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "ListShare_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "ListShare_token_key" ON "ListShare"("token");
CREATE INDEX "ListShare_listId_idx" ON "ListShare"("listId");
ALTER TABLE "ListShare" ADD CONSTRAINT "ListShare_listId_fkey" FOREIGN KEY ("listId") REFERENCES "ProductList"("id") ON DELETE CASCADE ON UPDATE CASCADE;
