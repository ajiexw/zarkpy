#coding=utf-8
from Insert import Insert
import site_helper as sh

class Update(Insert):

    def POST(self, inputs=None):
        self._update(inputs)
        return sh.refresh()

    def _update(self, inputs=None):
        if inputs is None: inputs = self.initInputs(inputs)
        assert inputs.has_key('model_name'), '请指明需要修改的数据类型'
        assert inputs.has_key('model_id'),   '请指明需要修改的数据id'
        assert sh.session.is_login, '请先登录'
        model = sh.model(inputs.model_name)
        exists = model.get(inputs.model_id)
        if exists is not None:
            assert exists.get('Userid', 0) == sh.session.id, '您不能修改别人的数据'
            return model.update(inputs.model_id, inputs)
        else:
            return 0