class Empresa:
    def __init__(self, nome, localizacao, pontos):
        self.nome = nome
        self.localizacao = localizacao
        self.pontos = pontos 
        self.reservas = []

    def reservar_ponto(self, carro_id, ponto_id, janela_inicio, janela_fim):
        reserva = {
            "carro_id": carro_id,
            "ponto_id": ponto_id,
            "janela_inicio": janela_inicio,
            "janela_fim": janela_fim
        }
        self.reservas.append(reserva)
        return {
            "mensagem": f"[{self.nome}] Reserva confirmada para o carro {carro_id} no ponto {ponto_id}."
        }

    def consultar_reservas(self):
        return self.reservas

    def cancelar_reserva(self, carro_id, ponto_id):
        for r in self.reservas:
            if r["carro_id"] == carro_id and r["ponto_id"] == ponto_id:
                self.reservas.remove(r)
                return {"mensagem": f"Reserva do carro {carro_id} no ponto {ponto_id} cancelada com sucesso."}
        return {"erro": "Reserva não encontrada."}

    def verificar_disponibilidade(self, ponto_id, janela_inicio, janela_fim):
        for r in self.reservas:
            if r["ponto_id"] == ponto_id:
                if not (janela_fim <= r["janela_inicio"] or janela_inicio >= r["janela_fim"]):
                    return {"disponivel": False, "mensagem": "Ponto indisponível nessa janela."}
        return {"disponivel": True, "mensagem": "Ponto disponível na janela informada."}
