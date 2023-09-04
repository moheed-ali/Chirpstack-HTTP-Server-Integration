from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from chirpstack_api import integration
from google.protobuf.json_format import Parse
import csv

class Handler(BaseHTTPRequestHandler):
    # True -  JSON marshaler
    # False - Protobuf marshaler (binary)
    json = True
    csv_filename = "data.csv"

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        query_args = parse_qs(urlparse(self.path).query)

        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)

        if query_args["event"][0] == "up":
            self.up(body)

        elif query_args["event"][0] == "join":
            self.join(body)

        else:
            print("handler for event %s is not implemented" % query_args["event"][0])

    def up(self, body):
        up = self.unmarshal(body, integration.UplinkEvent())
        print("Uplink received from: %s with F count: %s" % (up.device_info.device_name, up.f_cnt))

        # Extract values from the 'up' object
        row_data = [
            up.deduplication_id,
            up.time.seconds,
            up.device_info.tenant_id,
            up.device_info.tenant_name,
            up.device_info.application_id,
            up.device_info.application_name,
            up.device_info.device_profile_id,
            up.device_info.device_profile_name,
            up.device_info.device_name,
            up.device_info.dev_eui,
            # up.tags.key,
            up.dev_addr,
            up.dr,
            up.f_port,
            up.data.hex(),
            up.f_cnt
        ]

        # Extract rxInfo values
        rx_info_values = []
        for rx_info in up.rx_info:
            rx_info_values.append([
                rx_info.gateway_id,
                rx_info.uplink_id,
                rx_info.rssi,
                rx_info.snr,
                rx_info.context
            ])

        # Extract txInfo values
        if up.HasField('tx_info'):
            tx_info = up.tx_info
            tx_info_values = [
                tx_info.frequency,
                tx_info.modulation.lora.bandwidth,
                tx_info.modulation.lora.spreading_factor,
                tx_info.modulation.lora.code_rate
            ]
        else:
            tx_info_values = ["", "", "", ""]

        # Flatten the rx_info_values and append tx_info_values
        flattened_rx_info = [item for sublist in rx_info_values for item in sublist]
        row_data.extend(flattened_rx_info)
        row_data.extend(tx_info_values)

        # Check if the CSV file exists and write headers if not
        if not self.does_csv_exist():
            self.write_csv_headers()

        # Open the CSV file in append mode and write the row data
        with open(self.csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row_data)

    def join(self, body):
        join = self.unmarshal(body, integration.JoinEvent())
        print("Device: %s joined with DevAddr: %s" % (join.device_info.dev_eui, join.dev_addr))

    def unmarshal(self, body, pl):
        if self.json:
            return Parse(body, pl)

        pl.ParseFromString(body)
        return pl

    def does_csv_exist(self):
        try:
            with open(self.csv_filename, 'r'):
                return True
        except FileNotFoundError:
            return False

    def write_csv_headers(self):
        header_row = [
            "Deduplication ID",
            "Time Seconds",
            "Tenant ID",
            "Tenant Name",
            "Application ID",
            "Application Name",
            "Device Profile ID",
            "Device Profile Name",
            "Device Name",
            "Dev EUI",
            # "Tags Key",
            "Dev Addr",
            "Dr",
            "fPort",
            "Data Hex",
            "F Count",
            "rxInfo Gateway ID",
            "rxInfo Uplink ID",
            "rxInfo RSSI",
            "rxInfo SNR",
            "rxInfo Context",
            "txInfo Frequency",
            "Modulation-lora txInfo Bandwidth",
            "Modulation-lora Spreading Factor",
            "Modulation-lora Code Rate"
        ]

        with open(self.csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header_row)

httpd = HTTPServer(('', 8081), Handler)
httpd.serve_forever()
