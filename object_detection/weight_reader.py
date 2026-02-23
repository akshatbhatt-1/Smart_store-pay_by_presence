import serial
import threading


class WeightReader:
    def __init__(self, port="COM5", baudrate=57600, alpha=0.2):
        self.alpha = alpha
        self.filtered_weight = None
        self.running = True

        self.ser = serial.Serial(port, baudrate, timeout=1)

        self.thread = threading.Thread(target=self._read_loop)
        self.thread.daemon = True
        self.thread.start()

    def _read_loop(self):
        while self.running:
            try:
                line = self.ser.readline().decode().strip()

                if line:
                    raw = float(line)

                    if self.filtered_weight is None:
                        self.filtered_weight = raw
                    else:
                        self.filtered_weight = (
                            self.alpha * raw +
                            (1 - self.alpha) * self.filtered_weight
                        )

            except:
                pass

    def get_weight(self):
        return self.filtered_weight

    def stop(self):
        self.running = False
        self.ser.close()