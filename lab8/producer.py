from flask import Flask, request, jsonify, render_template_string
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import time
import threading

app = Flask(__name__)

TOPIC = "car_events"

producer = None
messages = []  # храним прочитанные сообщения в памяти


# ===================== KAFKA PRODUCER =====================
def get_producer():
    global producer
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=["kafka:9092"],
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("[PRODUCER] Connected to Kafka")
        except NoBrokersAvailable:
            print("[PRODUCER] Kafka not ready, retrying in 3s...")
            time.sleep(3)
    return producer


# ===================== KAFKA CONSUMER =====================
def start_consumer():
    message_count = 0

    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=["kafka:9092"],
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id="web-consumer",
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            print("[CONSUMER] Connected to Kafka, waiting for messages...")

            for msg in consumer:
                message_count += 1
                messages.append(msg.value)

                print(
                    f"[CONSUMER] Message #{message_count} | "
                    f"car_id={msg.value.get('car_id')} | "
                    f"event={msg.value.get('event')} | "
                    f"speed={msg.value.get('speed')}"
                )

        except NoBrokersAvailable:
            print("[CONSUMER] Kafka not ready, retrying in 3s...")
            time.sleep(3)


threading.Thread(target=start_consumer, daemon=True).start()


# ===================== WEB UI =====================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kafka Web Interface</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 8px; margin: 5px 0; width: 300px; }
        button { cursor: pointer; }
        table { border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px 12px; }
        th { background: #f2f2f2; }
    </style>
</head>
<body>

<h2>Send event to Kafka</h2>

<form id="form">
    <input id="car_id" placeholder="Car ID" required><br>
    <input id="event" placeholder="Event" required><br>
    <input id="speed" placeholder="Speed"><br>
    <button type="submit">Send</button>
</form>

<h2>Messages from Kafka</h2>

<table>
    <thead>
        <tr>
            <th>Car ID</th>
            <th>Event</th>
            <th>Speed</th>
        </tr>
    </thead>
    <tbody id="table-body"></tbody>
</table>

<script>
async function loadMessages() {
    const res = await fetch("/messages");
    const data = await res.json();

    const tbody = document.getElementById("table-body");
    tbody.innerHTML = "";

    data.forEach(msg => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${msg.car_id ?? ""}</td>
            <td>${msg.event ?? ""}</td>
            <td>${msg.speed ?? ""}</td>
        `;
        tbody.appendChild(row);
    });
}

document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        car_id: document.getElementById("car_id").value,
        event: document.getElementById("event").value,
        speed: document.getElementById("speed").value
    };

    await fetch("/send", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    document.getElementById("form").reset();
    loadMessages();
});

loadMessages();
setInterval(loadMessages, 3000);
</script>

</body>
</html>
"""


# ===================== ROUTES =====================
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/send", methods=["POST"])
def send():
    data = request.json
    p = get_producer()
    p.send(TOPIC, data)
    p.flush()
    return jsonify({"status": "sent", "data": data})


@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(messages[-50:])  # последние 50 сообщений


@app.route("/health")
def health():
    return {"status": "ok"}


# ===================== START =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
