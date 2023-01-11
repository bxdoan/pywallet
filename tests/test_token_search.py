from unittest import TestCase

from pywallet.token import TokenSearch


class TokenSearchTest(TestCase):

    def test_token_search(self):
        # Test token search by symbol
        list_tokens = TokenSearch(search_key='AAVE').search()
        assert len(list_tokens) == 80

        val_EXPECT = {
            'symbol': 'AAVE', 'name': 'Aave', 'type': 'ERC20', 'address': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9',
            'ens_address': '', 'decimals': 18, 'website': 'https://app.aave.com/?referral=93',
            'logo': {'src': '', 'width': '', 'height': '', 'ipfs_hash': ''}, 'support': {'email': '', 'url': ''},
            'social': {
                'blog': '', 'chat': '', 'discord': '', 'facebook': '', 'forum': '', 'github': '', 'gitter': '',
                'instagram': '', 'linkedin': '', 'reddit': '', 'slack': '', 'telegram': '',
                'twitter': '', 'youtube': ''
            }
        }
        assert val_EXPECT in list_tokens

    def test_token_search_w_network(self):
        list_tokens = TokenSearch(
            search_key='AAVE',
            network='bsc'
        ).search()
        assert len(list_tokens) == 1
        val_EXPECT = {
            'symbol': 'AAVE', 'name': 'Aave', 'type': 'ERC20', 'address': '0xfb6115445Bff7b52FeB98650C87f44907E58f802',
            'ens_address': '', 'decimals': 18, 'website': '',
            'logo': {'src': '', 'width': '', 'height': '', 'ipfs_hash': ''},
            'support': {'email': '', 'url': ''},
            'social': {
                'blog': '', 'chat': '', 'discord': '', 'facebook': '', 'forum': '', 'github': '', 'gitter': '',
                'instagram': '', 'linkedin': '', 'reddit': '', 'slack': '', 'telegram': '', 'twitter': '',
                'youtube': ''
            }
        }
        assert val_EXPECT in list_tokens
