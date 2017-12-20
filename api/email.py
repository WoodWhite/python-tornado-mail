# -*- coding: utf-8 -*-
import json
import logging as log

from tornado import gen
from tornado.queues import Queue
from tornado.web import RequestHandler

from decorator import xxx_except
from lib.mail import HtmlSmtpMail

queue = Queue(maxsize=128)

CREATE_EMAIL_OK = {'Code': 1000, 'Message': 'Create email ok!'}
CREATE_EMAIL_ERROR = {'Code': 2000, 'Message':'Create email error!'}


class EmailHandler(RequestHandler):

    SUPPORTED_METHODS = ('POST',)

    @gen.coroutine
    @xxx_except(CREATE_EMAIL_ERROR)
    def post(self, *args):

        def get_chronos_job_state(subject):
            return subject.split()[-1].replace('!', '').replace('.', '').capitalize()

        def get_chronos_job_message(state, message):
            if 'Failed' == state:
                errorInfo = message.split('The scheduler provided this message:')[-1]
                if 'Failed to launch container' in errorInfo and 'Cannot connect to the Docker daemon' in errorInfo:
                    return 'Docker服务异常'
                elif 'Failed to launch container' in errorInfo and 'Failed to fetch all URIs for container' in errorInfo:
                    return 'URIs错误或文件不存在'
                elif 'Failed to launch container' in errorInfo and 'is not a valid repository/tag' in errorInfo:
                    return '镜像地址无效'
                elif 'Failed to launch container' in errorInfo and 'connection refused' in errorInfo:
                    return 'Harbor地址错误或域名解析失败'
                elif 'Failed to launch container' in errorInfo and 'no such host' in errorInfo and 'pulling image' in errorInfo:
                    return 'Harbor地址错误或域名解析失败'
                elif 'Failed to launch container' in errorInfo and 'not found' in errorInfo and 'image' in errorInfo:
                    return '镜像不存在'
                elif 'Container exited' in errorInfo:
                    return '容器运行异常退出'
                elif 'Command exited' in errorInfo:
                    return '任务运行异常退出'
                elif 'Abnormal executor termination' in errorInfo:
                    return '容器运行异常终止'
                else:
                    return '未知错误，请联系研发'
            elif 'Disabled' == state:
                errorInfo = message.split('The scheduler provided this message:')[-1]
                if 'Failed to launch container' in errorInfo and 'connection refused' in errorInfo:
                    return 'Harbor地址错误或域名解析失败'
                elif 'Container exited' in errorInfo:
                    return '容器运行异常退出'
                elif 'Command exited' in errorInfo:
                    return '任务运行异常退出'
                elif 'Failed to launch container' in errorInfo and 'no such host' in errorInfo and 'pulling image' in errorInfo:
                    return 'Harbor地址错误或域名解析失败'
                elif 'Abnormal executor termination' in errorInfo:
                    return '容器运行异常终止'
                elif 'has exhausted all of its recurrences and has been disabled.' in message:
                    return
                else:
                    return '未知错误，请联系研发'
            elif 'Deleted' == state:
                # return '任务被删除'
                return
            else:
                return '未知状态，请联系研发'

        data = json.loads(self.request.body.decode('utf8'))
        if args:
            if 'xxxxxx' == args[0]:
                email = self.settings.get('email_conf')['xxxxxx']
                state = get_chronos_job_state(data.get('subject', ''))
                message = get_chronos_job_message(state, data.get('message', ''))
                if not message:
                    return
                email['content_type'] = 'html'
                email['content'] = self.render_string(
                    template_name='chronos.html', platform=self.get_argument('platform', ''),
                    service=self.get_argument('service'), data_center=self.get_argument('data_center', ''),
                    task_name=data.get('job', ''), message=message, state=state
                    )
                yield queue.put(email)
            elif 'tmpfs' == args[0]:
                email = data
                email['content_type'] = 'html'
                email['content'] = self.render_string(
                    template_name='tmpfs.html', platform=data['content'].get('platform', ''),
                    service=data['content'].get('service', ''), ip=data['content'].get('ip', ''),
                    state=data['content'].get('state', ''), message=data['content'].get('message', '')
                    )
                yield queue.put(email)
            else:
                return

        else:
            data['content_type'] = 'json'
            yield queue.put(data)
        log.info('[code: 1000] Create email ok! body{%s}' % ''.join(self.request.body.split()))
        self.write(CREATE_EMAIL_OK)


@gen.coroutine
def handle_notify():
    while True:
        email = yield queue.get()
        try:
            em = HtmlSmtpMail(smtp_server=email['smtp_server'], smtp_user=email['smtp_user'],
                         smtp_password=email['smtp_password'], from_addr=email['from_addr'],
                         to_addr=email['to_addr'], subject=email['subject'])
            yield em.send_mail(email['content'], email['content_type'])
            log.info('[code: 1000] Send email ok! body{%s}' % ''.join(json.dumps(email).split()))
        except Exception as e:
            log.error('[code: 2000] Send email error! body{%s} by [%s]' % (''.join(json.dumps(email).split()), e))
        finally:
            queue.task_done()