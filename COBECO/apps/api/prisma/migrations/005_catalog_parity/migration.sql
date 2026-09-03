-- Catálogo normalizado e persistência do resultado do motor de paridade.
CREATE TABLE "Category" (
  "id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  CONSTRAINT "Category_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "Category_name_key" ON "Category"("name");

CREATE TABLE "Supplier" (
  "id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "categoryId" TEXT NOT NULL,
  "active" BOOLEAN NOT NULL DEFAULT true,
  CONSTRAINT "Supplier_pkey" PRIMARY KEY ("id")
);

CREATE INDEX "Supplier_categoryId_active_idx" ON "Supplier"("categoryId", "active");

CREATE TABLE "Product" (
  "id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "categoryId" TEXT NOT NULL,
  "unit" TEXT NOT NULL DEFAULT 'unidade',
  "active" BOOLEAN NOT NULL DEFAULT true,
  CONSTRAINT "Product_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "Product_categoryId_name_key" ON "Product"("categoryId", "name");
CREATE INDEX "Product_categoryId_active_idx" ON "Product"("categoryId", "active");

CREATE TABLE "SupplierProduct" (
  "supplierId" TEXT NOT NULL,
  "productId" TEXT NOT NULL,
  "price" DECIMAL(10,2) NOT NULL,
  "active" BOOLEAN NOT NULL DEFAULT true,
  CONSTRAINT "SupplierProduct_pkey" PRIMARY KEY ("supplierId", "productId")
);

CREATE INDEX "SupplierProduct_productId_active_idx" ON "SupplierProduct"("productId", "active");

ALTER TABLE "ProductList" ADD COLUMN "categoryId" TEXT;
ALTER TABLE "ListItem" ADD COLUMN "productId" TEXT;
ALTER TABLE "Quotation" ADD COLUMN "parityGroups" JSONB;
ALTER TABLE "Quotation" ADD COLUMN "parityMeta" JSONB;
ALTER TABLE "Quotation" ADD COLUMN "bestGroupId" TEXT;

CREATE INDEX "ProductList_categoryId_idx" ON "ProductList"("categoryId");
CREATE INDEX "ListItem_productId_idx" ON "ListItem"("productId");

ALTER TABLE "Supplier" ADD CONSTRAINT "Supplier_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category"("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "Product" ADD CONSTRAINT "Product_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category"("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "SupplierProduct" ADD CONSTRAINT "SupplierProduct_supplierId_fkey" FOREIGN KEY ("supplierId") REFERENCES "Supplier"("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "SupplierProduct" ADD CONSTRAINT "SupplierProduct_productId_fkey" FOREIGN KEY ("productId") REFERENCES "Product"("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "ProductList" ADD CONSTRAINT "ProductList_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "ListItem" ADD CONSTRAINT "ListItem_productId_fkey" FOREIGN KEY ("productId") REFERENCES "Product"("id") ON DELETE SET NULL ON UPDATE CASCADE;
