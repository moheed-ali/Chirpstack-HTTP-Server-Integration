# Chirpstack-HTTP-Server-Integration

This repository contains code to integrate ChirpStack (LoRaWAN Network Server) with an HTTP server and store event data in a CSV file. The integration is designed to handle "up" and "join" events from ChirpStack devices.

For more information on ChirpStack HTTP integration, please refer to the [ChirpStack Documentation](https://www.chirpstack.io/docs/chirpstack/integrations/http.html#http).

## Prerequisites

- ChirpStack server is up and running.
- HTTP integration is added to the ChirpStack application.
- Python 3.7+ is installed.

## Setup and Usage

1. **Clone this repository:**

    ```bash
    git clone https://github.com/your-username/Chirpstack-HTTP-Server-Integration.git
    cd Chirpstack-HTTP-Server-Integration
    ```

2. **Activate the virtual environment (venv):**

    ```bash
    source venv/bin/activate
    ```

3. **Run the main.py script to start the HTTP integration server:**

    ```bash
    python main.py
    ```

    This script listens for incoming ChirpStack events, processes "up" and "join" events, and stores data in a CSV file.

4. **Ensure that ChirpStack is sending events to the HTTP integration server.** Make sure to configure the ChirpStack application's HTTP integration settings to point to your server's address and port.

## Project Structure

Chirpstack-HTTP-Server-Integration/
│
├── main.py
├── venv/
└── HTTP Server Test Example/
├── req.py
└── test.py


- `main.py`: Contains the HTTP integration code for handling ChirpStack events and storing data in a CSV file.
- `venv/`: Virtual environment directory.
- `HTTP Server Test Example/`: Example scripts for testing the HTTP server.
    - `req.py`: Sends a POST request to the HTTP server.
    - `test.py`: Creates a basic HTTP server for testing.

## Contributing

Feel free to contribute to this project by creating pull requests. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the [MIT License](LICENSE).
