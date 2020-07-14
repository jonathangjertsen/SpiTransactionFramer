from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

class SpiTransactionFramer(HighLevelAnalyzer):
    result_types = {
        "SpiTransaction": {
            "format": "MISO: {{data.miso}}, MOSI: {{data.mosi}}"
        }
    }

    def __init__(self):
        self.frames = []
        self.spi_enabled = False
        self.frame_start_time = None
        self.error = False

    def handle_enable(self, frame):
        self.spi_enable = True
        self.frame_start_time = frame.start_time

    def reset(self):
        self.spi_enable = False
        self.frames = []
        self.error = False

    def handle_result(self, frame):
        if self.spi_enable:
            self.frames.append(frame)

    def get_frame_data(self):
        miso = bytearray()
        mosi = bytearray()

        for frame in self.frames:
            miso += frame.data["miso"]
            mosi += frame.data["mosi"]

        return {
            "miso": bytes(miso),
            "mosi": bytes(mosi),
        }

    def handle_disable(self, frame):
        if self.spi_enable and not self.error:
            result = AnalyzerFrame(
                "SpiTransaction",
                self.frame_start_time,
                frame.end_time,
                self.get_frame_data(),
            )
        else:
            result = None

        self.reset()
        return result

    def handle_error(self, frame):
        self.reset()

    def decode(self, frame: AnalyzerFrame):
        if frame.type == "enable":
            return self.handle_enable(frame)
        elif frame.type == "result":
            return self.handle_result(frame)
        elif frame.type == "disable":
            return self.handle_disable(frame)
        elif frame.type == "error":
            return self.handle_error(frame)
        else:
            raise ValueError(frame)