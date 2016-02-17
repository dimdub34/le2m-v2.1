# -*- coding: utf-8 -*-

from twisted.spread import pb
from twisted.internet import defer
import logging
from datetime import datetime
import random
from util.utili18n import le2mtrans
from questcomp.questcompgui import GuiQuestCompQuest
from client.cltgui.cltguidialogs import GuiAccueil, GuiPopup, GuiFinal, \
    GuiQuestionnaireFinal
from questcomp.questcompmod import Question, CopyQuestion
import clttexts


logger = logging.getLogger("le2m")


class IRemote(pb.Referenceable):
    """
    This is an interface, used by every remote part
    """
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self._histo = []
        self._currentperiod = 0
        self._payoff_ecus = 0
        self._payoff_euros = 0
        self._payoff_text = u""

    @property
    def le2mclt(self):
        return self._le2mclt

    @property
    def histo(self):
        return self._histo

    @property
    def currentperiod(self):
        return self._currentperiod

    @currentperiod.setter
    def currentperiod(self, val):
        self._currentperiod = val

    @property
    def payoff_ecus(self):
        return self._payoff_ecus

    @payoff_ecus.setter
    def payoff_ecus(self, val):
        self._payoff_ecus = val

    @property
    def payoff_euros(self):
        return self._payoff_euros

    @payoff_euros.setter
    def payoff_euros(self, val):
        self._payoff_euros = val

    @property
    def payoff_text(self):
        return self._payoff_text

    @payoff_text.setter
    def payoff_text(self, val):
        self._payoff_text = val

    def remote_set_payoffs(self, in_euros, in_ecus=None):
        logger.debug(u"{} set_payoffs".format(self.le2mclt.uid))
        self.payoff_euros = in_euros
        self.payoff_ecus = in_ecus
        self.payoff_text = clttexts.get_payoff_text(
            self.payoff_euros, self.payoff_ecus)

    def remote_display_payoffs(self):
        logger.debug(u"{} display_payoffs".format(self.le2mclt.uid))
        return self.le2mclt.get_remote("base").remote_display_information(
            self.payoff_text)


class RemoteBase(pb.Root):
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt

    def remote_load_parts(self, parts):
        """
        This method is called by servparties.PartieBase
        This method try to import the modules corresponding to the parts given
        as argument and to create an instance of the remote object of this
        module.
        :param parts: a list where each item is a dict with 3 keys:
        remote_partie_name, remote_classname
        """
        logger.info(u"{} Parts to load: {p}".format(self._le2mclt.uid, parts))
        for p in parts:
            if self._le2mclt.get_remote(p):
                continue  # the part is already loaded
            if self._le2mclt.load_remotepart(p):
                logger.info(u"{} Part {} loaded".format(
                    p["remote_partie_name"]))
            else:
                logger.critical(
                    le2mtrans(u"Error while loading part {p}").format(p=p))
    
    def remote_set_simulation(self, value):
        self._le2mclt.simulation = value
        return self._le2mclt.simulation

    def remote_set_automatique(self, value):
        self._le2mclt.automatique = value
        return self._le2mclt.automatique

    def remote_display_welcome(self):
        """ Affichage de l'écran d'accueil sur le poste 
        Cet écran a un bouton "instructions lues" sur lequel les sujets 
        cliquent lorsqu'ils ont fini de lire les instructions.
        """
        logger.info(u"{} Welcome".format(self._le2mclt.uid))
        if self._le2mclt.simulation: 
            logger.info(u"{} Send back 1".format(self._le2mclt.uid))
            return 1
        else:
            defered = defer.Deferred()
            ecran_accueil = GuiAccueil(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            ecran_accueil.show()
            return defered

    def remote_disconnect(self):
        """
        The remote will disconnect from the server and the application (remote
        side) will exit
        """
        logger.info(u"{} Disconnect".format(self._le2mclt.uid))
        try:
            if self._finalscreen.isVisible():
                self._finalscreen.accept()
        except AttributeError:
            pass
        self._le2mclt.disconnect()
        return 1

    def remote_get_remote(self, partname, remoteclassname):
        """
        Return the remote of the part
        :param partname:
        :param remoteclassname:
        :return: Remote instance
        """
        logger.info(u"{} get_remote".format(self._le2mclt.uid))
        remote = self._le2mclt.get_remote(partname)
        if not remote:
            self._le2mclt.load_part(partname, remoteclassname)
            remote = self._le2mclt.get_remote(partname)
        return remote

    def remote_display_questcomp(self, question):
        """
        Display the understanding question and return 1 if the subject
        gives a wrong answer, 0 otherwise
        :param question
        :return: Deferred
        """
        logger.info(u"{} Question {}".format(self._le2mclt.uid, question))
        if self._le2mclt.simulation:
            return random.randint(0, 1)  # faute ou non au hasard
        else:
            defered = defer.Deferred()
            ecran = GuiQuestCompQuest(
                defered, self._le2mclt.automatique, question,
                self._le2mclt.screen)
            ecran.show()
            return defered
            
    def remote_display_information(self, txt):
        """
        Display the information in a qmessagebox
        :param txt: the text to be displayed
        """
        logger.info(u"Information: {}".format(txt))
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            if self._le2mclt.automatique:
                popup = GuiPopup(defered, txt, 7000, self._le2mclt.screen)
            else:
                popup = GuiPopup(defered, txt, 0, self._le2mclt.screen)
            popup.show()
            return defered

    def remote_display_finalscreen(self, final_payoff):
        if type(final_payoff) is str:
            txt = final_payoff
        else:
            txt = clttexts.get_final_text(final_payoff)
        logger.info(u'Payoff: {}'.format(txt))
        if self._le2mclt.simulation:
            return le2mtrans(u"This a comment from the simulation mode")
        else:
            defered = defer.Deferred()
            self._finalscreen = GuiFinal(
                defered, self._le2mclt.automatique, self._le2mclt.screen, txt)
            self._finalscreen.show()
            return defered
            
    def remote_display_popup(self, txt, temps=10000):
        logger.info(u"{} Popup {}".format(self._le2mclt.uid, txt))
        if self._le2mclt.simulation:
            return 1
        else: 
            popup = GuiPopup(
                txt, temps, self._le2mclt.screen)
            popup.show()
            return 1
            
    # def remote_display_partpayoffs(self, partname):
    #     remote = self._le2mclt.get_remote(partname)
    #     if not remote:
    #         logger.error(u"{} ".format(partname) +
    #                      le2mtrans(u"is not in the remote list of parts"))
    #         return
    #     else:
    #         return self.remote_display_information(remote.payoff_text)

    def remote_display_payoffs(self, list_of_parts):
        txt = u""
        for i, p in enumerate(list_of_parts):
            remote = self._le2mclt.get_remote(p)
            if remote:
                txt += le2mtrans(u"Part") + u" {}: ".format(i+1) + \
                    remote.payoff_text + u"\n"
        return self.remote_display_information(txt)


class RemoteQuestionnaireFinal(pb.Referenceable):
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self._nom = 'questionnaireFinal'
    
    def remote_demarrer(self):
        logger.info(u"Affichage du questionnaire final")
        if self._le2mclt.simulation:
            inputs = {}
            today_year = datetime.now().year
            inputs['naissance'] = today_year - random.randint(16,  60)
            inputs['genre'] = random.randint(0, 1)
            inputs['nationalite'] = random.randint(1, 100)
            inputs['couple'] = random.randint(0, 1)
            inputs['etudiant'] = random.randint(0, 1)
            if inputs['etudiant']:
                inputs['etudiant_discipline'] = random.randint(1, 10)
                inputs['etudiant_niveau'] = random.randint(1, 6)
            inputs['experiences'] = random.randint(0, 1)
            inputs["fratrie_nombre"] = random.randint(0, 10)
            if inputs["fratrie_nombre"] > 0:
                inputs["fratrie_rang"] = random.randint(
                    1, inputs["fratrie_nombre"] + 1)
            else: inputs["fratrie_rang"] = 0
            # sportivité
            inputs["sportif"] = random.randint(0, 1)
            if inputs["sportif"]:
                inputs["sportif_type"] = random.randint(0, 1)
                inputs["sportif_competition"] = random.randint(0, 1)
            # religiosité
            inputs['religion_place'] = random.randint(1, 4)
            inputs['religion_croyance'] = random.randint(1, 4)
            inputs['religion_nom'] = random.randint(1, 6)
            logger.info(u"Renvoi: {}".format(inputs))
            return inputs
        else:
            defered = defer.Deferred()
            screen = GuiQuestionnaireFinal(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            screen.show()
            return defered


class ReceiverQuestion(pb.RemoteCopy, Question):
    """
    This is for handling the questions of the understanding questionnaire
    We say to twisted that this is a secure object
    """
    pass
pb.setUnjellyableForClass(CopyQuestion, ReceiverQuestion)