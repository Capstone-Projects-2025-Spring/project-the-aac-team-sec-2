import { useEffect, useState } from "react";

const WebSocketDemo = () => {
    const [messages, setMessages] = useState([]);
    const [ws, setWs] = useState(null);
    const [message, setMessage] = useState("");
    const [playerId, setPlayerId] = useState(1);
    const [card, setCard] = useState(1);

    useEffect(() => {
        const socket = new WebSocket("ws://localhost:8000/ws");
		addMessage("Attempting to connect to WebSocket...");

        socket.onopen = () => addMessage("Connected to WebSocket");
        socket.onmessage = (event) => addMessage(event.data);
        socket.onclose = () => addMessage("WebSocket closed");

        setWs(socket);

        return () => socket.close();
    }, []);

    const addMessage = (msg) => {
        setMessages((prev) => [...prev, msg]);
    };

    const sendMessage = () => {
        ws.send(JSON.stringify({ data: { type: "chat", message }, source_player_id: 0 }));
        setMessage("");
		addMessage(`[Client] Chat sent: "${message}"`);
    };

    const sendQuery = () => {
        ws.send(JSON.stringify({ data: { type: "query", target_player_id: playerId, card: card }, source_player_id: 0 }));
		addMessage(`[Client] Game action sent: "Player ${playerId}, got any ${card}s?"`);
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    };

	const isWebSocketConnecting = ws && ws.readyState === WebSocket.CONNECTING;

    return (
        <div>
            <h3>Chat</h3>
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a message..."
            />
            <button onClick={sendMessage} disabled={isWebSocketConnecting}>Send</button>

            <h3>Got any...</h3>
            Player:
            <input
                type="range"
                min="1"
                max="4"
                value={playerId}
                onChange={(e) => setPlayerId(e.target.value)}
            />
            <span> {playerId}</span>
            <br />
            Card:
            <input
                type="range"
                min="1"
                max="10"
                value={card}
                onChange={(e) => setCard(e.target.value)}
            />
            <span> {card}</span>
            <br />
            <button onClick={sendQuery} disabled={isWebSocketConnecting}>Send</button>

			<h3>Event Log</h3>
			<div>
                {messages.map((msg, idx) => (
                    <div key={idx}>{msg}</div>
                ))}
            </div>
        </div>
    );
};

export default WebSocketDemo;
