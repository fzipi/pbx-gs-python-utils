from pbx_gs_python_utils.plantuml.API_Plant_UML import API_Plant_UML
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Misc import Misc


class Puml:
    def __init__(self):
        self.puml        = ""
        self.api_plantuml = API_Plant_UML()

        self.available_elements   = ["actor"   , "agent"    , "artifact"  ,"boundary" , "card"      , "cloud"   , "component" ,
                                     "control" , "database" , "entity"    , "file"    , "folder"    , "frame"   , "interface" ,
                                     "node"    , "package"  , "queue"     , "stack"   , "rectangle" , "storage" , "usecase"   ]
        self.available_directions = ['up', 'down','left','right']
        self.on_add_node           = None
        self.on_add_edge           = None
        self.max_title             = 40

    def add_card     (self, title, id = None) : return self.add_node("card", title, id)
    def add_cloud    (self, title, id = None) : return self.add_node("cloud", title, id)
    def add_actor    (self, title, id = None) : return self.add_node("actor", title, id)
    def add_interface(self, title, id = None) : return self.add_node("interface", title, id)

    def add_node(self, element, title, id = None):

        title = Misc.word_wrap_escaped(title, self.max_title)

        if self.on_add_node:                                                      # if self.on_add_element is set, then use it for the node render bit
            puml_to_add = self.on_add_node(element,title,self.fix_id(id),id)
            if puml_to_add:
                self.puml += "\t{0} \n".format(puml_to_add)
        else:
            if id:
                self.puml += '\t{0} "{1}" as {2} \n'.format(element, title, self.fix_id(id))
            else:
                self.puml += '\t{0} "{1}"\n'        .format(element, title)
        return self

    def add_edge(self, from_id, to_id, direction = 'down', label=""):
        self.puml += '\t{0} -{2}-> {1} : "{3}" \n'.format(self.fix_id(from_id), self.fix_id(to_id), direction ,label)
        return self

    def add_line(self, line):
        self.puml += "\t{0}\n".format(line)
        return self

    def startuml(self):
        self.puml += "@startuml\n"
        return self


    def enduml(self):
        self.puml += "@enduml\n"
        return self

    def fix_id(self, id):
        if id:
            return id.replace(' ','_').replace('-','_').replace(':','_').replace('/','_').replace('(','_').replace(')','_')

    def png(self, path = None):
        if path:
            self.api_plantuml.tmp_png_file = path
        self.api_plantuml.puml_to_png(self.puml)
        return self

    def save(self, path):
        Files.write(path,self.puml)
        return self

    def save_tmp(self):
        tmp_path_png = '/tmp/test_simple_diagram.png'
        tmp_path_puml = '/tmp/test_simple_diagram.puml'
        ( self.png(tmp_path_png)
              .save(tmp_path_puml) )
        return tmp_path_png,tmp_path_puml

    def set_on_add_node(self, callback): self.on_add_node = callback ; return self
    def set_on_add_edge(self, callback): self.on_add_edge = callback ; return self

    # def show(self):
    #     self.api_plantuml.show(self.puml)

    def __str__(self):
        return self.puml

    # other util method to be used during developemt

    def _dev_send_to_slack(self):
        from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
        API_Slack().puml_to_slack(self.puml)



