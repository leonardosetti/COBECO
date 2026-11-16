# COBECO Backend — Value Objects Unit Tests
# Testes para Value Objects: Email, CNPJ, SenhaHash, UnidadeMedida

import pytest
from src.domain.entities import Email, CNPJ, SenhaHash, UnidadeMedida


class TestEmail:
    """Testes para Value Object Email"""

    def test_email_valido_lowercase(self):
        email = Email("Teste@Exemplo.COM")
        assert email.valor == "teste@exemplo.com"

    def test_email_valido_com_espacos(self):
        email = Email("  usuario@dominio.com  ")
        assert email.valor == "usuario@dominio.com"

    def test_email_invalido_sem_arroba(self):
        with pytest.raises(ValueError, match="Email inválido"):
            Email("usuario.dominio.com")

    def test_email_invalido_sem_dominio(self):
        with pytest.raises(ValueError, match="Email inválido"):
            Email("usuario@")

    def test_email_invalido_sem_ponto_no_dominio(self):
        with pytest.raises(ValueError, match="Email inválido"):
            Email("usuario@dominio")

    def test_email_invalido_vazio(self):
        with pytest.raises(ValueError, match="Email inválido"):
            Email("")

    def test_email_invalido_none(self):
        with pytest.raises((ValueError, TypeError)):
            Email(None)


class TestCNPJ:
    """Testes para Value Object CNPJ"""

    def test_cnpj_valido_apenas_digitos(self):
        cnpj = CNPJ("12345678000195")
        assert cnpj.valor == "12345678000195"

    def test_cnpj_valido_com_formatacao(self):
        cnpj = CNPJ("12.345.678/0001-95")
        assert cnpj.valor == "12.345.678/0001-95"

    def test_cnpj_invalido_menos_digitos(self):
        with pytest.raises(ValueError, match="CNPJ deve ter 14 dígitos"):
            CNPJ("1234567800019")

    def test_cnpj_invalido_mais_digitos(self):
        with pytest.raises(ValueError, match="CNPJ deve ter 14 dígitos"):
            CNPJ("123456780001951")

    def test_cnpj_invalido_letras(self):
        with pytest.raises(ValueError, match="CNPJ deve ter 14 dígitos"):
            CNPJ("12.345.678/0001-AB")

    def test_cnpj_invalido_vazio(self):
        with pytest.raises(ValueError, match="CNPJ deve ter 14 dígitos"):
            CNPJ("")


class TestSenhaHash:
    """Testes para Value Object SenhaHash"""

    def test_senha_hash_cria_corretamente(self):
        hash_valor = "$2b$12$abcdefghijklmnopqrstuv"
        senha_hash = SenhaHash(hash_valor)
        assert senha_hash.valor == hash_valor

    def test_senha_hash_aceita_string_vazia(self):
        # Value object não valida conteúdo, apenas armazena
        senha_hash = SenhaHash("")
        assert senha_hash.valor == ""


class TestUnidadeMedida:
    """Testes para Enum UnidadeMedida"""

    def test_unidades_disponiveis(self):
        assert UnidadeMedida.UN == "un"
        assert UnidadeMedida.KG == "kg"
        assert UnidadeMedida.L == "L"
        assert UnidadeMedida.M == "m"

    def test_unidade_medida_e_str(self):
        # UnidadeMedida is a StrEnum, so str() returns the enum member name
        assert str(UnidadeMedida.UN) == "un"
        assert UnidadeMedida.UN.value == "un"
        assert isinstance(UnidadeMedida.KG, str)

    def test_unidade_medida_comparacao(self):
        assert UnidadeMedida.UN == "un"
        assert UnidadeMedida.KG != "un"
