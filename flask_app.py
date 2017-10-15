from flask import Flask , request, jsonify, Response, make_response
import subprocess
import rocksdb
import hashlib
app = Flask(__name__)

#db = rocksdb.DB("/tmp/test.db", rocksdb.Options(create_if_missing=True))

@app.route('/api/v1/scripts', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print("post command received")
        db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
        f = request.files['data']
        key = int(hashlib.sha256(f.filename.encode('utf-8')).hexdigest(), 16) % 10 ** 8
        f.save("results/"+f.filename)
        db.put(str(key).encode('utf-8'), f.filename.encode('utf-8'))
        print("post command received %s %s" %(str(key),f.filename))
        list = {}
        list["script-id"]=key
        return make_response(jsonify(list), 201)

@app.route('/api/v1/scripts/<script>', methods=['GET'])
def execute_file(script):
    if request.method =='GET':
        db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
        val = db.get(str(script).encode('utf-8'))
        print("GET command received %s %s " %(str(script),val))
        with open("output.txt", "w+") as output:
            subprocess.call(["python3.6", "results/"+val.decode('utf-8')], stdout=output);
        with open("output.txt") as f:
            content = f.readlines()
            print("".join(content))
        return Response("".join(content) , status = 200)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=True)
