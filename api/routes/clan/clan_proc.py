from flask import Blueprint, Response, request
import message_diffusion as md


clan_proc = Blueprint('clan_proc', __name__)


@clan_proc.route('/clan/diffusion/send')
def send_diffusion():
    try:
        md_controller = md.MessageDiffusion()
        md_controller.start_diffusion()
        return Response("Message sent to servers...")
    except KeyError as e:
        print(e)
        return e
