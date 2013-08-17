#coding=utf-8
# ../../page/user/Login.html
import site_helper as sh

class Login:

    def GET(self):
        action = sh.getEnv('REQUEST_URI').partition('?')[0].strip('/')
        if action == 'login':
            return sh.page.user.Login()
        if action == 'logout':
            sh.ctrl('User').logout()
            return sh.redirect('/')

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        assert(inputs.get('email', '').strip())
        assert(inputs.get('password', ''))

        uc = sh.ctrl('User')
        model = sh.model('User')
        action = sh.getEnv('REQUEST_URI').partition('?')[0].strip('/')

        if action == 'login':
            if not uc.validate(inputs.email, inputs.password):
                return sh.page.user.Login('您输入的用户名或密码不对, 请重新输入', inputs.email)

            user = model.getByEmail(inputs.email)

            if user.dead == 'yes':
                return sh.alert('登录失败,你已被列入黑名单,请联系管理员')

            uc.login(user, inputs.get('remember_me', '') == 'on')

            # 获得打开login页面时url中指定的referer
            referer = sh.getUrlParams(sh.getEnv('HTTP_REFERER')).get('referer', None)
            if referer:
                return sh.redirect(referer)
            elif sh.inputs().get('referer', None):
                return sh.redirect(sh.inputs().get('referer', None))
            else:
                return sh.redirect('/')
