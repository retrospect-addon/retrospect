# ===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
# ===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA. 
# ===============================================================================

import sys

import xbmc


class LockWithDialog(object):
    """ Decorator Class that locks a method using a busy dialog """

    BusyDialog = "busydialognocancel" if int(xbmc.getInfoLabel("system.buildversion").split(".")[0]) >= 18 else "busydialog"

    @staticmethod
    def close_busy_dialog():
        """ Closes any BusyDialog if one is open. """

        xbmc.executebuiltin("Dialog.Close({0})".format(LockWithDialog.BusyDialog))
        return

    def __init__(self, logger=None):
        """ Initializes the decorator with a specific method.

        We need to use the Decorator as a function @LockWithDialog() to get the
        'self' parameter passed on.

        :param logger: A Kodi Logger object

        """

        self.logger = logger
        return

    def __call__(self, wrapped_function):
        """ When the method is called this is executed.

        :param function wrapped_function: The function that is wrapped in the
                                          LockWithDialog decorator

        :return: the function that wraps the wrapped_function
        :rtype: function

        """

        def __inner_wrapped_function(*args, **kwargs):
            """ Function that get's called instead of the decorated function """

            # show the busy dialog
            if self.logger:
                self.logger.Debug("Locking interface and showing '%s'", LockWithDialog.BusyDialog)

            xbmc.executebuiltin("ActivateWindow({0})".format(LockWithDialog.BusyDialog))
            try:
                response = wrapped_function(*args, **kwargs)
                # time.sleep(2)
            except Exception:
                # re-raise the exception with the original traceback info
                # see http://nedbatchelder.com/blog/200711/rethrowing_exceptions_in_python.html
                error_info = sys.exc_info()
                raise error_info[1], None, error_info[2]

            finally:
                # Hide the busy Dialog
                LockWithDialog.close_busy_dialog()
                if self.logger:
                    self.logger.Debug("Un-locking interface and hiding '%s'",
                                      LockWithDialog.BusyDialog)
            return response

        return __inner_wrapped_function
