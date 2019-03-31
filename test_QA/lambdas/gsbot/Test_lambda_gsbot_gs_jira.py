import unittest

from   pbx_gs_python_utils.lambdas.gsbot.gsbot_gs_jira import run
from   pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class test_lambda_gsbot_gs_jira(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambdas('pbx_gs_python_utils.lambdas.gsbot.gsbot_gs_jira', memory = 3008)

    #def test_lambda_update(self):
    #    self.step_lambda.update_with_lib()

    def test_invoke_directly(self):
        response = run({},{})
        assert response == None


    def _send_command_message(self,command):
        payload = {'params' : [command] , 'data': {'team_id':'T7F3AUXGV', 'channel':'GDL2EC3EE'}}
        return self.step_lambda.invoke(payload)          # see answer in slack, or add a return to line 17 (in lambda_gs_bot)

    def test_invoke(self):
        response = self._send_command_message('help')
        assert response == [ ':red_circle: command not found `help`\n'
                              '\n'
                              '*Here are the `GS_Bot_Jira_Commands` commands available:*',
                              [ { 'actions': [],
                                  'callback_id': '',
                                  'color': 'good',
                                  'fallback': None,
                                  'text': ' • issue\n • projects\n • update\n'}]]
