from flask import Flask, request
from wol import wake_machine

app = Flask(__name__)
PASSWORD = "nCqBcs5XFfYZtCrQwA3XxQczMGReXM5jkgh23fOT"


@app.route('/wake', methods=['POST'])
def wake():
    args = dict(request.form)
    if not ('ip' in args) or not ('password' in args):
        return "Unauthorized, key 'ip' or 'password' is missing.", 403
    elif args.get('password') != PASSWORD:
        return "Password incorrect.", 401
    else:
        try:
            wake_machine(args['ip'])
        except Exception as e:
            return f"Failed to send the magic packet: {str(e)}"
        else:
            return f"Magic packet sent to {args['ip']}.", 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=38051)
