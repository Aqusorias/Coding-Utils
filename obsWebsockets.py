import sys
import time
from obswebsocket import obsws, requests


''' -Information: SETUP: in obs, go to Tools -> WebSockets Server Settings -> Enable WebSockets Server checkbox. Server Port 4455, Password: OBSWebSocketPassword
Import: `from obsWebsockets import OBSWebsocketsManager`
Initialize: `obswebsockets_manager = OBSWebsocketsManager()`

>>:-  pip install obs-websocket-py

Usage: 
1. obswebsockets_manager.set_source_visibility(scene_name, source_name, source_visible=True)            // Activate or deactivate a source (e.g. an image)
2. obswebsockets_manager.change_scene(scene_name)                                                       // Swap to a specific scene
3. obswebsockets_manager.set_filter_visibility(source_name, filter_name, filter_enabled=True)           // Activate or deactivate a filter (e.g. a chroma key)
4. obswebsockets_manager.get_scene_items(scene_name)                                                    // Get a list of all soruces in a scene
5. obswebsockets_manager.disconnect()                                                                   // Disconnect from OBS

scene_name = Name of the target scene
source_name = Name of the target source
filter_name = Name of the target filter
source_visible = True: Source will be visible, False: Source will be invisible
filter_enabled = True: Filter will be enabled, False: Filter will be disabled
'''


class OBSWebsocketsManager:
    
    def __init__(self):
        self.ws = obsws("localhost", 4455, "OBSWebSocketPassword")
        try:
            self.ws.connect()
        except:
            print("COULD NOT CONNECT TO OBS!\nDouble check that you have OBS open and that your websockets server is enabled in OBS.")
            time.sleep(10)
            sys.exit()
        print("Successfully connected to OBS Websockets!\n")


    def change_scene(self, scene_name):
        self.ws.call(requests.SetCurrentProgramScene(sceneName=scene_name))


    def set_source_visibility(self, scene_name, source_name, source_visible=True):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        myItemID = response.datain['sceneItemId']
        self.ws.call(requests.SetSceneItemEnabled(sceneName=scene_name, sceneItemId=myItemID, sceneItemEnabled=source_visible))


    def set_filter_visibility(self, source_name, filter_name, filter_enabled=True):
        self.ws.call(requests.SetSourceFilterEnabled(sourceName=source_name, filterName=filter_name, filterEnabled=filter_enabled))


    def get_scene_items(self, scene_name):
        return self.ws.call(requests.GetSceneItemList(sceneName=scene_name))


    def disconnect(self):
        self.ws.disconnect()


if __name__ == '__main__':
  exit("Do not run this file directly")
