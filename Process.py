import multiprocess

class SimpleProcessManager:
    def __init__(self):
        self.process = None

    def create_process(self, target, args=()):
        self.process = multiprocess.Process(daemon=True,target=target, args=args)

    def start_process(self):
        if self.process:
            self.process.start()

    def get_process_status(self):
        if self.process:
            return f"Process {self.process.pid} is running: {self.process.is_alive()}"
        else:
            return "No process created."

    def terminate_process(self):
        if self.process:
            self.process.terminate()
            self.process.join()

