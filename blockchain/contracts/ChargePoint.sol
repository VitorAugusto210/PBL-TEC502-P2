// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ChargePoint
 * @dev Contrato para gerenciar o registro de sessões de recarga de VEs
 * em um ledger distribuído, garantindo transparência e segurança.
 */
contract ChargePoint {

    // Estrutura para armazenar os dados de cada sessão de recarga
    struct ChargingSession {
        address user;           // Endereço do usuário que fez a reserva
        uint256 stationId;      // Identificador da estação de recarga
        uint256 startTime;      // Timestamp do início da reserva
        uint256 endTime;        // Timestamp do fim da recarga
        uint256 energyConsumed; // Energia consumida em Wh (Watt-hora)
        uint256 cost;           // Custo final em Wei
        bool isPaid;            // Status do pagamento
        bool exists;            // Indica se a sessão é válida
    }

    // Mapeamento do ID da sessão para os seus dados
    mapping(uint256 => ChargingSession) public sessions;
    
    // --- CONTROLE DE CONCORRÊNCIA ---
    // Mapeamento para controlar o estado de cada estação (livre/ocupada)
    mapping(uint256 => bool) public estacaoEstaReservada;

    // Contador para o próximo ID de sessão disponível
    uint256 public nextSessionId;

    // Eventos para notificar aplicações externas sobre mudanças de estado
    event ReservationCreated(uint256 indexed sessionId, address indexed user, uint256 stationId);
    event RechargeFinished(uint256 indexed sessionId, uint256 energyConsumed, uint256 cost);
    event PaymentMade(uint256 indexed sessionId);
    event ReservationCancelled(uint256 indexed sessionId);

    // Inicializa o contrato definindo o primeiro ID de sessão como 1
    constructor() {
        nextSessionId = 1;
    }

    /**
     * @dev Cria uma nova reserva e a registra no blockchain.
     * Trava a estação para impedir reservas concorrentes.
     * @param _user O endereço da carteira do usuário.
     * @param _stationId O ID da estação que está sendo reservada.
     * @return O ID da nova sessão de recarga criada.
     */
    function createReservation(address _user, uint256 _stationId) public returns (uint256) {
        // VERIFICAÇÃO DE CONCORRÊNCIA: Garante que a estação não esteja já reservada.
        require(!estacaoEstaReservada[_stationId], "Erro: Estacao de recarga ja esta reservada.");

        // TRAVA O RECURSO: Marca a estação como reservada.
        estacaoEstaReservada[_stationId] = true;

        uint256 sessionId = nextSessionId;
        sessions[sessionId] = ChargingSession({
            user: _user,
            stationId: _stationId,
            startTime: block.timestamp,
            endTime: 0,
            energyConsumed: 0,
            cost: 0,
            isPaid: false,
            exists: true
        });
        
        nextSessionId++;
        emit ReservationCreated(sessionId, _user, _stationId);
        return sessionId;
    }

    /**
     * @dev Finaliza uma sessão de recarga, registrando consumo e custo.
     * Libera a estação para que possa ser reservada novamente.
     * @param _sessionId O ID da sessão a ser finalizada.
     * @param _energyConsumed A quantidade de energia consumida.
     * @param _cost O custo final da recarga.
     */
    function finishRecharge(uint256 _sessionId, uint256 _energyConsumed, uint256 _cost) public {
        ChargingSession storage session = sessions[_sessionId];
        require(session.exists, "Erro: Sessao nao existe.");
        require(session.endTime == 0, "Erro: Recarga ja finalizada.");

        session.endTime = block.timestamp;
        session.energyConsumed = _energyConsumed;
        session.cost = _cost;

        // LIBERA O RECURSO: Marca a estação como livre novamente.
        estacaoEstaReservada[session.stationId] = false;

        emit RechargeFinished(_sessionId, _energyConsumed, _cost);
    }

    /**
     * @dev Cancela uma reserva que ainda não foi iniciada (ou seja, não foi finalizada).
     * @param _sessionId O ID da sessão a ser cancelada.
     */
    function cancelReservation(uint256 _sessionId) public {
        ChargingSession storage session = sessions[_sessionId];
        require(session.exists, "Erro: Sessao nao existe.");
        // Garante que só o usuário que reservou pode cancelar
        require(msg.sender == session.user, "Erro: Apenas o usuario da reserva pode cancelar.");
        require(session.endTime == 0, "Erro: Nao e possivel cancelar uma recarga ja finalizada.");

        // LIBERA O RECURSO: Marca a estação como livre novamente.
        estacaoEstaReservada[session.stationId] = false;

        // Invalida a sessão para que não possa ser usada futuramente
        session.exists = false;

        emit ReservationCancelled(_sessionId);
    }

    /**
     * @dev Registra um pagamento para uma sessão de recarga.
     * A função é 'payable', o que permite que ela receba Ether.
     * @param _sessionId O ID da sessão a ser paga.
     */
    function makePayment(uint256 _sessionId) public payable {
        ChargingSession storage session = sessions[_sessionId];
        require(session.exists, "Erro: Sessao nao existe.");
        require(!session.isPaid, "Erro: Sessao ja foi paga.");
        require(msg.value >= session.cost, "Erro: Valor enviado e insuficiente para cobrir o custo.");

        session.isPaid = true;

        // Lógica opcional para transferir os fundos para a carteira da empresa.
        // address payable companyWallet = payable(owner);
        // companyWallet.transfer(msg.value);

        emit PaymentMade(_sessionId);
    }

    /**
     * @dev Função de leitura para obter os detalhes de uma sessão.
     * @param _sessionId O ID da sessão a ser consultada.
     * @return Os dados da sessão.
     */
    function getSession(uint256 _sessionId) public view returns (address, uint256, uint256, uint256, uint256, uint256, bool) {
        require(sessions[_sessionId].exists, "Erro: Sessao nao existe.");
        ChargingSession storage session = sessions[_sessionId];
        return (
            session.user,
            session.stationId,
            session.startTime,
            session.endTime,
            session.energyConsumed,
            session.cost,
            session.isPaid
        );
    }
}