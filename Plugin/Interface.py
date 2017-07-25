from Core.Database import Database
from Core.Error import Error
from Core.File import File
from Core.Msg import Msg
from Core.Text import Text
import re
import sys

class Interface(object):

    def __init__(self, cfg, pluginParams, workflowPluginParams, frameworkParams):
        self.__cfg = cfg
        self.__pluginParams = pluginParams
        self.__workflowPluginParams = workflowPluginParams
        self.__frameworkParams = frameworkParams

    def getAnalyzerContent(self):
        return self.__getContent("analyzerPath")

    def getAnalyzerContentFromDatabase(self):
        NotImplemented

    def getCfgValue(self, name):
        return self.__cfg[name]

    def __getContent(self, inputType):
        return File.getContent(self.__frameworkParams[inputType])

    def getFrameworkParamValue(self, name):
        return self.__frameworkParams[name]

    def getInputContent(self):
        return self.__getContent("inputPath")

    def getInputContentFromDatabase(self):
        NotImplemented

    def getOutputContent(self):
        return self.__getContent("outputPath")

    def getOutputContentFromDatabase(self):
        NotImplemented

    def getPluginParamValue(self, name):
        return self.__pluginParams[name]

    def getPluginParamValueAsInt(self, name):
        return int(self.getPluginParamValue(name))

    def getPluginParamValueAsTrueOrFalse(self, name):
        return Text.toTrueOrFalse(self.getPluginParamValue(name))

    def getTranslatorContent(self):
        return self.__getContent("translatorPath")

    def getTranslatorContentFromDatabase(self):
        NotImplemented

    def getTranslatorContentAsSections(self):
        content = self.getTranslatorContent()
        sectionizedContent = {"VOCABULARY": [], "REJECTED": [], "L1": [], "L2": []}
        for token in content.split("\n"):
            token = token.strip()
            if len(token) < 1 or re.match("#", token):
                continue
            if re.search("(VOCABULARY|REJECT|L1|L2)", token):
                if token == "[VOCABULARY]":
                    vocabularyFlag = True
                    rejectedFlag = False
                    l1Flag = False
                    l2Flag = False
                elif token == "[REJECTED]":
                    vocabularyFlag = False
                    rejectedFlag = True
                    l1Flag = False
                    l2Flag = False
                elif token == "[L1]":
                    vocabularyFlag = False
                    rejectedFlag = False
                    l1Flag = True
                    l2Flag = False
                elif token == "[L2]":
                    vocabularyFlag = False
                    rejectedFlag = False
                    l1Flag = False
                    l2Flag = True
                continue
            if vocabularyFlag:
                sectionizedContent["VOCABULARY"].append(token)
            elif rejectedFlag:
                sectionizedContent["REJECTED"].append(token)
            elif l1Flag:
                sectionizedContent["L1"].append(token)
            elif l2Flag:
                sectionizedContent["L2"].append(token)
        for key in sectionizedContent.keys():
            sectionizedContent[key] = "\n".join(sectionizedContent[key])
        return sectionizedContent

    def getWorkflowSource(self):
        return self.__workflowPluginParams["__workflowSourcePath__"]
        #if "Source" in self.__workflowPluginParams:
        #    return self.__workflowPluginParams["Source"]
        #return None

    def getWorkflowTarget(self):
        return self.__workflowPluginParams["__workflowTargetPath__"]
        #if "Target" in self.__workflowPluginParams:
        #    return self.__workflowPluginParams["Target"]
        #return None

    def handleException(msg, showStackTraceFlag=True, abortFlag=True):
        Error.handleException(msg, showStackTraceFlag, abortFlag)

    def raiseException(self, msg):
        Error.raiseException(msg)

    def setAnalyzerContent(self, content):
        return self.__setContent("analyzerPath", content)

    def __setContent(self, outputType, content):
        return File.setContent(self.__frameworkParams[outputType], content)

    def setInputContent(self, content):
        return self.__setContent("inputPath", content)

    def setOutputContent(self, content):
        content = self.__setContent("outputPath", content)
        File.copy(self.__frameworkParams["outputPath"], self.getWorkflowTarget())
        return content

    def setTranslatorContent(self, content):
        return self.__setContent("translatorPath", content)

    def show(self):
        Msg.showRaw("Configuration")
        Msg.showPretty(self.__cfg)
        Msg.showRaw("Plugin Parameters")
        Msg.showPretty(self.__pluginParams)
        Msg.showRaw("Framework Parameters")
        Msg.showPretty(self.__frameworkParams)