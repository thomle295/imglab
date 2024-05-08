from flask import request, Flask, flash, Response, send_from_directory
import json
import os
from werkzeug.utils import secure_filename
import base64

class Api():
    def __init__(self):
        self.root_path = os.path.join(os.getcwd(),"datas")
        
    def save_file(self):
            if request.method == "POST":
                ###check json in data######
                if "json" not in request.form:
                    return Response(json.dumps({"error":" do not have file "}),status=500,mimetype="application/json")
                ###get string data####
                f = request.form["json"]
                # print(f)


                ###convert string to json
                json_data = json.loads(f)

                ##get name of file####
                name = request.form["filename"]
                # print(name)

                ### find image in  images list json from data is sent from client
                json_data_to_write = {}
                idx=0
                for imgname in json_data["images"]:
                    if name in imgname["file_name"]:
                        json_data_to_write["images"] = imgname
                        idx = imgname["id"]
                        break
                
                ##### add type to json
                json_data_to_write["type"] = json_data["type"]
                            
                ##### ad categories to json
                json_data_to_write["categories"] = json_data["categories"]

                #### add annotations of image to json
                json_data_to_write["annotations"] = []
                for segment in json_data["annotations"]:
                    if segment["image_id"] == idx:
                        json_data_to_write["annotations"].append(segment)
                # print(name)
                ### create id folder
                dataId = name.split("-")[:-1]
                dataId = "-".join(dataId)
                name = name.split("-")[-1]
                
                path = os.path.join(self.root_path,dataId)
                ####create json file name
                jsonname = name+".json"
                ### check id folder is exists
                if not os.path.exists(path):
                    os.mkdir(path)
                ### write json file
                with open(os.path.join(path,jsonname),"w") as f:
                    json.dump(json_data_to_write,f)
  

                ### create image file name
                image_name = name+".jpg"
                
                ## get image data
                if "imgs" in request.form:
                    
                    img = request.form["imgs"]
                    ### decode base64
                    img = img.split("base64,")[-1]
                    imgdata = base64.b64decode(img)
                    # save image to id folder
                    with open(os.path.join(path,image_name), 'wb') as f:
                        f.write(imgdata)
                
                
                ### return success
                return Response(json.dumps({"success":"save completely"}), status=200, mimetype="application/json")
    def ping(self):
        if request.method == "GET":
            return Response(json.dumps({"success":"ping success"}), status=200, mimetype="application/json")