from unittest import TestCase
from alexaaudioqueue import AlexaAudioQueue


class TestAlexaAudioQueue(TestCase):
    def test_no_loop(self):
        urls = ["a", "b"]
        queue = AlexaAudioQueue(urls, loop_tracks=False, shuffle_tracks=False)
        self.assertTrue(queue.start() is "a")
        self.assertTrue(queue.next() is "b")
        self.assertTrue(queue.next() is None)

    def test_loop(self):
        urls = ["a", "b"]
        queue = AlexaAudioQueue(urls, loop_tracks=True, shuffle_tracks=False)
        self.assertTrue(queue.start() is "a")
        self.assertTrue(queue.next() is "b")
        self.assertTrue(queue.next() is "a")
        self.assertTrue(queue.next() is "b")

    def test_shuffle_no_loop(self):
        urls = ["a", "b", "c", "d", "e", "f", "g"]
        queue = AlexaAudioQueue(urls, loop_tracks=False, shuffle_tracks=True)
        play_order = []
        play_order.append(queue.start())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        self.assertFalse(play_order is urls)
        self.assertTrue(queue.next() is None)

    def test_shuffle_with_loop(self):
        urls = ["a", "b", "c", "d", "e", "f", "g"]
        queue = AlexaAudioQueue(urls, loop_tracks=True, shuffle_tracks=True)
        play_order = []
        play_order.append(queue.start())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        play_order.append(queue.next())
        self.assertFalse(play_order is urls)

        play_order_second = []
        play_order_second.append(queue.next())
        play_order_second.append(queue.next())
        play_order_second.append(queue.next())
        play_order_second.append(queue.next())
        play_order_second.append(queue.next())
        play_order_second.append(queue.next())
        play_order_second.append(queue.next())
        self.assertFalse(play_order_second is urls)
        self.assertFalse(play_order_second is play_order)

    def test_next(self):
        urls = ["a", "b", "c"]
        queue = AlexaAudioQueue(urls, loop_tracks=True, shuffle_tracks=False)
        self.assertTrue(queue.start() is "a")
        self.assertTrue(queue.current is "a")
        self.assertTrue(queue.up_next() is "b")
        queue.next()
        self.assertTrue(queue.current is "b")
        self.assertTrue(queue.up_next() is "c")
        queue.next()
        self.assertTrue(queue.current is "c")
        self.assertTrue(queue.up_next() is "a")
        queue.next()
        self.assertTrue(queue.current is "a")
        self.assertTrue(queue.up_next() is "b")


if __name__ == '__main__':
    unittest.main()

