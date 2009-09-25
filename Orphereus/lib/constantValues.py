################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################


from pylons.i18n import _, ungettext, N_

decimalVersion = "1.2.5"
engineVersion = "Orphereus %s" % decimalVersion

id3FieldsNames = {
"album" : N_("Album"),
"title" : N_("Title"),
"artist" : N_("Artist"),
}

LOG_EVENT_SECURITY_IP = 0x00000001
LOG_EVENT_INVITE = 0x00010001
LOG_EVENT_INVITE_USED = 0x00010002
LOG_EVENT_BOARD_EDIT = 0x00020001
LOG_EVENT_BOARD_DELETE = 0x00020002
LOG_EVENT_USER_EDIT = 0x00030001
LOG_EVENT_USER_DELETE = 0x00030002
LOG_EVENT_USER_ACCESS = 0x00030003
LOG_EVENT_USER_BAN = 0x00030004
LOG_EVENT_USER_UNBAN = 0x00030005
LOG_EVENT_USER_GETUID = 0x00030006
LOG_EVENT_USER_PASSWD = 0x00030007
LOG_EVENT_SETTINGS_EDIT = 0x00040001
LOG_EVENT_POSTS_DELETE = 0x00050001
LOG_EVENT_EXTENSION_EDIT = 0x00060001
LOG_EVENT_MTN_BEGIN = 0x00070001
LOG_EVENT_MTN_END = 0x00070002
LOG_EVENT_MTN_UNBAN = 0x00070002
LOG_EVENT_MTN_DELINVITE = 0x00070003
LOG_EVENT_MTN_ERROR = 0x00070003
LOG_EVENT_RICKROLLD = 0x00080001
LOG_EVENT_EDITEDPOST = 0x00090001
LOG_EVENT_INTEGR = 0x00100000
LOG_EVENT_INTEGR_RC = 0x00100001
LOG_EVENT_BAN_ADD = 0x00110001
LOG_EVENT_BAN_DISABLE = 0x00110002
LOG_EVENT_BAN_REMOVE = 0x00110003
LOG_EVENT_BAN_EDIT = 0x00110004

disabledEvents = [LOG_EVENT_RICKROLLD, LOG_EVENT_SECURITY_IP, LOG_EVENT_INTEGR]

destinations = {0 : N_("Thread"),
                1 : N_("First page of current board"),
                2 : N_("Current page of current board"),
                3 : N_("Overview"),
                4 : N_("First page of destination board"),
                5 : N_("Referrer"),
                }

CFG_BOOL = 0x01
CFG_INT = 0x02
CFG_STRING = 0x04
CFG_LIST = 0x08
