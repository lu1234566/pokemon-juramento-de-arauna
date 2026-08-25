import socket
import threading
import unittest

from arauna_qa.protocol import MgbaBridge, key_mask


class ProtocolTests(unittest.TestCase):
    def test_key_masks_match_gba_layout(self):
        self.assertEqual(key_mask("A"), 1 << 0)
        self.assertEqual(key_mask("UP"), 1 << 6)
        self.assertEqual(key_mask(["LEFT", "B"]), (1 << 5) | (1 << 1))

    def test_request_response_round_trip(self):
        client, server = socket.socketpair()
        bridge = MgbaBridge(client)

        def peer():
            try:
                data = b""
                while b"\n" not in data:
                    data += server.recv(4096)
                line = data.decode("utf-8").strip()
                request_id, command = line.split("\t", 1)
                self.assertEqual(command, "PING")
                server.sendall(f"{request_id}\tOK\tPONG\n".encode("utf-8"))
            finally:
                server.close()

        thread = threading.Thread(target=peer)
        thread.start()
        try:
            self.assertTrue(bridge.ping())
        finally:
            bridge.close()
            thread.join(timeout=2)
        self.assertFalse(thread.is_alive())


if __name__ == "__main__":
    unittest.main()
