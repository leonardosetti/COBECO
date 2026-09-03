CREATE INDEX "Quotation_userId_requestedAt_idx" ON "Quotation"("userId", "requestedAt");
CREATE INDEX "QuotationResult_providerSlug_fetchedAt_idx" ON "QuotationResult"("providerSlug", "fetchedAt");
