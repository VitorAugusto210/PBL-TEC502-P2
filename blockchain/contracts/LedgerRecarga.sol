// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LedgerRecarga {

    struct Reserva {
        uint256 idReserva;
        string carroId;
        string pontoId;
        string empresaId; // Pode ser o nome da empresa ou um identificador
        uint256 janelaInicio; // Timestamp Unix
        uint256 janelaFim;    // Timestamp Unix
        bool existe; // Para verificar se uma reserva com este ID foi criada
    }

    // Mapeamento do ID da reserva para a struct Reserva
    mapping(uint256 => Reserva) public reservas;

    // Contador para gerar IDs de reserva únicos
    uint256 public proximoIdReserva;

    // Evento emitido quando uma nova reserva é registrada
    event ReservaRegistrada(
        uint256 idReserva,
        string carroId,
        string pontoId,
        string empresaId,
        uint256 janelaInicio,
        uint256 janelaFim
    );

    constructor() {
        proximoIdReserva = 1; // Começa o ID da reserva em 1
    }

    /**
     * @dev Registra uma nova reserva no ledger.
     * @param _carroId ID do carro.
     * @param _pontoId ID do ponto de recarga.
     * @param _empresaId ID da empresa proprietária do ponto.
     * @param _janelaInicio Timestamp Unix do início da janela de reserva.
     * @param _janelaFim Timestamp Unix do fim da janela de reserva.
     */
    function registrarReserva(
        string calldata _carroId,
        string calldata _pontoId,
        string calldata _empresaId,
        uint256 _janelaInicio,
        uint256 _janelaFim
    ) public returns (uint256) {
        require(_janelaInicio < _janelaFim, "Janela de inicio deve ser anterior a janela de fim");
        require(bytes(_carroId).length > 0, "ID do carro nao pode ser vazio");
        require(bytes(_pontoId).length > 0, "ID do ponto nao pode ser vazio");

        uint256 idAtual = proximoIdReserva;

        reservas[idAtual] = Reserva({
            idReserva: idAtual,
            carroId: _carroId,
            pontoId: _pontoId,
            empresaId: _empresaId,
            janelaInicio: _janelaInicio,
            janelaFim: _janelaFim,
            existe: true
        });

        emit ReservaRegistrada(idAtual, _carroId, _pontoId, _empresaId, _janelaInicio, _janelaFim);

        proximoIdReserva++;
        return idAtual;
    }

    /**
     * @dev Retorna os detalhes de uma reserva dado o seu ID.
     * @param _idReserva O ID da reserva a ser consultada.
     * @return Os detalhes da reserva.
     */
    function getReserva(uint256 _idReserva) public view returns (Reserva memory) {
        require(reservas[_idReserva].existe, "Reserva nao encontrada");
        return reservas[_idReserva];
    }
}