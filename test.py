from donationalerts_api import DonationAlertsAPI
import webbrowser

api = DonationAlertsAPI("8575", "zDlWgu5tZpyLF6riPXts5bLko9LHsaM2esnHlMa5", "https://zwczslp151.lp151.com/", "oauth-user-show")

webbrowser.open(api.login())