// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ChargePoint {

    struct ChargingSession {
        address user;
        uint256 stationId;
        uint256 startTime;
        uint256 endTime;
        uint256 energyConsumed; // Em Wh
        uint256 cost;           // Custo em Wei
        bool isPaid;
        bool exists;
    }

    mapping(uint256 => ChargingSession) public sessions;
    uint256 public nextSessionId;

    event ReservationCreated(uint256 indexed sessionId, address indexed user, uint256 stationId);
    event RechargeFinished(uint256 indexed sessionId, uint256 energyConsumed, uint256 cost);
    event PaymentMade(uint256 indexed sessionId);

    constructor() {
        nextSessionId = 1;
    }

    function createReservation(address _user, uint256 _stationId) public returns (uint256) {
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

    function finishRecharge(uint256 _sessionId, uint256 _energyConsumed, uint256 _cost) public {
        require(sessions[_sessionId].exists, "Session does not exist");
        require(sessions[_sessionId].endTime == 0, "Recharge already finished");

        sessions[_sessionId].endTime = block.timestamp;
        sessions[_sessionId].energyConsumed = _energyConsumed;
        sessions[_sessionId].cost = _cost;

        emit RechargeFinished(_sessionId, _energyConsumed, _cost);
    }

    function makePayment(uint256 _sessionId) public payable {
        require(sessions[_sessionId].exists, "Session does not exist");
        require(!sessions[_sessionId].isPaid, "Session already paid");
        require(msg.value >= sessions[_sessionId].cost, "Insufficient payment");

        sessions[_sessionId].isPaid = true;

        // Lógica para transferir o pagamento para a empresa (se necessário)
        // address payable companyWallet = payable(owner);
        // companyWallet.transfer(msg.value);

        emit PaymentMade(_sessionId);
    }

    function getSession(uint256 _sessionId) public view returns (address, uint256, uint256, uint256, uint256, uint256, bool) {
        require(sessions[_sessionId].exists, "Session does not exist");
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