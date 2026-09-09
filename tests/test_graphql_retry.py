import importlib
import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault('ACCESS_TOKEN', 'test-token')
os.environ.setdefault('USER_NAME', 'test-user')
today = importlib.import_module('today')


class GraphqlRequestTests(unittest.TestCase):
    @patch('today.time.sleep')
    @patch('today.requests.post')
    def test_retries_502_then_succeeds_with_exponential_backoff(self, post, sleep):
        post.side_effect = [Mock(status_code=502, headers={}, text='bad gateway'),
                            Mock(status_code=200, headers={}, text='ok')]
        result = today.graphql_request('test', 'query', {})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(post.call_count, 2)
        sleep.assert_called_once_with(1)

    @patch('today.time.sleep')
    @patch('today.requests.post')
    def test_uses_retry_after_for_429(self, post, sleep):
        post.side_effect = [Mock(status_code=429, headers={'Retry-After': '3'}, text='slow down'),
                            Mock(status_code=200, headers={}, text='ok')]
        today.graphql_request('test', 'query', {})
        sleep.assert_called_once_with(3.0)

    @patch('today.time.sleep')
    @patch('today.requests.post')
    def test_does_not_retry_permanent_401_and_preserves_cache(self, post, sleep):
        post.return_value = Mock(status_code=401, headers={}, text='bad credentials')
        preserve = Mock()
        with self.assertRaises(Exception):
            today.graphql_request('test', 'query', {}, before_failure=preserve)
        self.assertEqual(post.call_count, 1)
        sleep.assert_not_called()
        preserve.assert_called_once_with()

    @patch('today.time.sleep')
    @patch('today.requests.post')
    def test_preserves_cache_after_transient_retries_are_exhausted(self, post, sleep):
        post.return_value = Mock(status_code=503, headers={}, text='unavailable')
        preserve = Mock()
        with self.assertRaises(Exception):
            today.graphql_request('test', 'query', {}, before_failure=preserve)
        self.assertEqual(post.call_count, today.MAX_REQUEST_ATTEMPTS)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [1, 2, 4])
        preserve.assert_called_once_with()


class StarsCounterTests(unittest.TestCase):
    @patch('builtins.print')
    def test_skips_null_node(self, print_mock):
        data = [
            {'node': None},
            {'node': {'stargazers': {'totalCount': 4}}},
        ]
        self.assertEqual(today.stars_counter(data), 4)
        print_mock.assert_called_once_with(
            'Star count entries ignored due to missing data:', 1
        )

    @patch('builtins.print')
    def test_skips_null_stargazers(self, print_mock):
        data = [
            {'node': {'stargazers': None}},
            {'node': {'stargazers': {'totalCount': 2}}},
        ]
        self.assertEqual(today.stars_counter(data), 2)
        print_mock.assert_called_once_with(
            'Star count entries ignored due to missing data:', 1
        )


if __name__ == '__main__':
    unittest.main()
