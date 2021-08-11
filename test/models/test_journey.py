import os
import hashlib
import random
import uuid
import json

import mock

from unittest import TestCase

from bike.constants import (
    STAGED_DATA_DIR,
    SENT_DATA_DIR
)
from bike.settings import (
    MINUTES_TO_CUT,
    EXCLUDE_METRES_BEGIN_AND_END
)
from bike.models.journey import Journey
from bike.models.frame import Frame


class JourneyTest(TestCase):

    def setUp(self):

        os.makedirs(
            STAGED_DATA_DIR,
            exist_ok=True
        )

        with open('test/resources/dublin_route.json') as json_file:
            self.test_data = json.load(json_file)

        self.test_journey = Journey()
        for d in self.test_data:
            self.test_journey.append(
                Frame(
                    d['time'],
                    {'lat': d['lat'], 'lng': d['lng']},
                    1  # acceleration, don't really care at the mo
                )
            )

    def test_route_graph(self):

        graph_coordinates = []
        for frame_uuid, frame_data in self.test_journey.route_graph._node.items():
            graph_coordinates.append(
                {
                    'lat': frame_data['y'],
                    'lng': frame_data['x']
                }
            )

        data_no_time = [{'lat': d['lat'], 'lng': d['lng']} for d in self.test_data]

        self.assertEqual(graph_coordinates, data_no_time)

        self.assertEqual(
            list(self.test_journey.route_graph._node.keys()),
            [frame.uuid for frame in self.test_journey]
        )

    def test_serialization(self):

        self.assertEqual(
            self.test_journey.serialize()['data'],
            [{'time': 0, 'acc': 1, 'gps': {'lat': 53.3588887, 'lng': -6.2530891, 'elevation': None}}, {'time': 10, 'acc': 1, 'gps': {'lat': 53.3584649, 'lng': -6.2533216, 'elevation': None}}, {'time': 20, 'acc': 1, 'gps': {'lat': 53.358193, 'lng': -6.253461, 'elevation': None}}, {'time': 30, 'acc': 1, 'gps': {'lat': 53.3581476, 'lng': -6.2534842, 'elevation': None}}, {'time': 40, 'acc': 1, 'gps': {'lat': 53.3579793, 'lng': -6.2526218, 'elevation': None}}, {'time': 50, 'acc': 1, 'gps': {'lat': 53.3579255, 'lng': -6.2523619, 'elevation': None}}, {'time': 60, 'acc': 1, 'gps': {'lat': 53.3577423, 'lng': -6.2525459, 'elevation': None}}, {'time': 70, 'acc': 1, 'gps': {'lat': 53.357707, 'lng': -6.2526408, 'elevation': None}}, {'time': 80, 'acc': 1, 'gps': {'lat': 53.3573489, 'lng': -6.2536058, 'elevation': None}}, {'time': 90, 'acc': 1, 'gps': {'lat': 53.3572005, 'lng': -6.2540083, 'elevation': None}}, {'time': 100, 'acc': 1, 'gps': {'lat': 53.3571312, 'lng': -6.2541836, 'elevation': None}}, {'time': 110, 'acc': 1, 'gps': {'lat': 53.3570936, 'lng': -6.2542868, 'elevation': None}}, {'time': 120, 'acc': 1, 'gps': {'lat': 53.3569809, 'lng': -6.2545955, 'elevation': None}}, {'time': 130, 'acc': 1, 'gps': {'lat': 53.3569514, 'lng': -6.2546764, 'elevation': None}}, {'time': 140, 'acc': 1, 'gps': {'lat': 53.3568576, 'lng': -6.2549334, 'elevation': None}}, {'time': 150, 'acc': 1, 'gps': {'lat': 53.3564663, 'lng': -6.2559997, 'elevation': None}}, {'time': 160, 'acc': 1, 'gps': {'lat': 53.3563727, 'lng': -6.2558978, 'elevation': None}}, {'time': 170, 'acc': 1, 'gps': {'lat': 53.3556449, 'lng': -6.257938, 'elevation': None}}, {'time': 180, 'acc': 1, 'gps': {'lat': 53.3550156, 'lng': -6.2574727, 'elevation': None}}, {'time': 190, 'acc': 1, 'gps': {'lat': 53.3549528, 'lng': -6.2574232, 'elevation': None}}, {'time': 200, 'acc': 1, 'gps': {'lat': 53.35465, 'lng': -6.257203, 'elevation': None}}, {'time': 210, 'acc': 1, 'gps': {'lat': 53.3541819, 'lng': -6.2568679, 'elevation': None}}, {'time': 220, 'acc': 1, 'gps': {'lat': 53.3539818, 'lng': -6.2577681, 'elevation': None}}, {'time': 230, 'acc': 1, 'gps': {'lat': 53.3538836, 'lng': -6.2581941, 'elevation': None}}, {'time': 240, 'acc': 1, 'gps': {'lat': 53.3538163, 'lng': -6.2584321, 'elevation': None}}, {'time': 250, 'acc': 1, 'gps': {'lat': 53.3535786, 'lng': -6.2591722, 'elevation': None}}, {'time': 260, 'acc': 1, 'gps': {'lat': 53.3534972, 'lng': -6.2594117, 'elevation': None}}, {'time': 270, 'acc': 1, 'gps': {'lat': 53.3533742, 'lng': -6.259676, 'elevation': None}}, {'time': 280, 'acc': 1, 'gps': {'lat': 53.3531925, 'lng': -6.2600954, 'elevation': None}}, {'time': 290, 'acc': 1, 'gps': {'lat': 53.3528433, 'lng': -6.2608812, 'elevation': None}}, {'time': 300, 'acc': 1, 'gps': {'lat': 53.3527764, 'lng': -6.2610318, 'elevation': None}}, {'time': 310, 'acc': 1, 'gps': {'lat': 53.352555, 'lng': -6.2613445, 'elevation': None}}, {'time': 320, 'acc': 1, 'gps': {'lat': 53.3519419, 'lng': -6.2610744, 'elevation': None}}, {'time': 330, 'acc': 1, 'gps': {'lat': 53.3503787, 'lng': -6.2603792, 'elevation': None}}, {'time': 340, 'acc': 1, 'gps': {'lat': 53.349819, 'lng': -6.260128, 'elevation': None}}, {'time': 350, 'acc': 1, 'gps': {'lat': 53.3488709, 'lng': -6.2597226, 'elevation': None}}, {'time': 360, 'acc': 1, 'gps': {'lat': 53.3484455, 'lng': -6.2595282, 'elevation': None}}, {'time': 370, 'acc': 1, 'gps': {'lat': 53.3483991, 'lng': -6.2595044, 'elevation': None}}, {'time': 380, 'acc': 1, 'gps': {'lat': 53.3475905, 'lng': -6.2591013, 'elevation': None}}, {'time': 390, 'acc': 1, 'gps': {'lat': 53.3470086, 'lng': -6.258792, 'elevation': None}}, {'time': 400, 'acc': 1, 'gps': {'lat': 53.3469351, 'lng': -6.25911, 'elevation': None}}, {'time': 410, 'acc': 1, 'gps': {'lat': 53.3468825, 'lng': -6.2593428, 'elevation': None}}, {'time': 420, 'acc': 1, 'gps': {'lat': 53.3467107, 'lng': -6.2600776, 'elevation': None}}, {'time': 430, 'acc': 1, 'gps': {'lat': 53.3465574, 'lng': -6.2607335, 'elevation': None}}, {'time': 440, 'acc': 1, 'gps': {'lat': 53.3462881, 'lng': -6.2618852, 'elevation': None}}, {'time': 450, 'acc': 1, 'gps': {'lat': 53.3461284, 'lng': -6.2626132, 'elevation': None}}, {'time': 460, 'acc': 1, 'gps': {'lat': 53.3456213, 'lng': -6.2625161, 'elevation': None}}, {'time': 470, 'acc': 1, 'gps': {'lat': 53.3456018, 'lng': -6.2628751, 'elevation': None}}, {'time': 480, 'acc': 1, 'gps': {'lat': 53.3448972, 'lng': -6.2627671, 'elevation': None}}, {'time': 490, 'acc': 1, 'gps': {'lat': 53.3448847, 'lng': -6.2633611, 'elevation': None}}, {'time': 500, 'acc': 1, 'gps': {'lat': 53.3442105, 'lng': -6.2633394, 'elevation': None}}, {'time': 510, 'acc': 1, 'gps': {'lat': 53.3441912, 'lng': -6.26387, 'elevation': None}}, {'time': 520, 'acc': 1, 'gps': {'lat': 53.3441799, 'lng': -6.2642788, 'elevation': None}}, {'time': 530, 'acc': 1, 'gps': {'lat': 53.3441775, 'lng': -6.2644509, 'elevation': None}}, {'time': 540, 'acc': 1, 'gps': {'lat': 53.3438399, 'lng': -6.26444, 'elevation': None}}, {'time': 550, 'acc': 1, 'gps': {'lat': 53.3429968, 'lng': -6.2644216, 'elevation': None}}, {'time': 560, 'acc': 1, 'gps': {'lat': 53.3421317, 'lng': -6.2646944, 'elevation': None}}, {'time': 570, 'acc': 1, 'gps': {'lat': 53.3414662, 'lng': -6.265404, 'elevation': None}}, {'time': 580, 'acc': 1, 'gps': {'lat': 53.3406712, 'lng': -6.2656141, 'elevation': None}}, {'time': 590, 'acc': 1, 'gps': {'lat': 53.3404613, 'lng': -6.2656749, 'elevation': None}}, {'time': 600, 'acc': 1, 'gps': {'lat': 53.3398737, 'lng': -6.2657997, 'elevation': None}}, {'time': 610, 'acc': 1, 'gps': {'lat': 53.3395894, 'lng': -6.2658639, 'elevation': None}}, {'time': 620, 'acc': 1, 'gps': {'lat': 53.3391577, 'lng': -6.2659588, 'elevation': None}}, {'time': 630, 'acc': 1, 'gps': {'lat': 53.338532, 'lng': -6.2661022, 'elevation': None}}, {'time': 640, 'acc': 1, 'gps': {'lat': 53.3383892, 'lng': -6.2660752, 'elevation': None}}, {'time': 650, 'acc': 1, 'gps': {'lat': 53.3377832, 'lng': -6.2658551, 'elevation': None}}, {'time': 660, 'acc': 1, 'gps': {'lat': 53.3376138, 'lng': -6.2657971, 'elevation': None}}, {'time': 670, 'acc': 1, 'gps': {'lat': 53.3374278, 'lng': -6.2657367, 'elevation': None}}, {'time': 680, 'acc': 1, 'gps': {'lat': 53.3369777, 'lng': -6.2656096, 'elevation': None}}, {'time': 690, 'acc': 1, 'gps': {'lat': 53.3364281, 'lng': -6.2654495, 'elevation': None}}, {'time': 700, 'acc': 1, 'gps': {'lat': 53.336174, 'lng': -6.2653568, 'elevation': None}}, {'time': 710, 'acc': 1, 'gps': {'lat': 53.3354833, 'lng': -6.2652056, 'elevation': None}}, {'time': 720, 'acc': 1, 'gps': {'lat': 53.3347258, 'lng': -6.2652546, 'elevation': None}}, {'time': 730, 'acc': 1, 'gps': {'lat': 53.3341412, 'lng': -6.2652779, 'elevation': None}}, {'time': 740, 'acc': 1, 'gps': {'lat': 53.333871, 'lng': -6.2651742, 'elevation': None}}, {'time': 750, 'acc': 1, 'gps': {'lat': 53.3337555, 'lng': -6.265012, 'elevation': None}}, {'time': 760, 'acc': 1, 'gps': {'lat': 53.3335892, 'lng': -6.2650038, 'elevation': None}}, {'time': 770, 'acc': 1, 'gps': {'lat': 53.332599, 'lng': -6.2647978, 'elevation': None}}]
        )
        self.assertEqual(
            self.test_journey.serialize()['direct_distance'],
            3024.84802816048
        )
        self.assertEqual(
            self.test_journey.serialize()['duration'],
            770
        )
        self.assertEqual(
            self.test_journey.serialize()['indirect_distance'],
            {
                1: 3734.354622435669,
                5: 3734.354622435669,
                10: 3734.354622435669,
                30: 3410.250751428646
            }
        )
        self.assertEqual(
            self.test_journey.serialize()['data_quality'],
            0.0
        )
        self.assertEqual(
            self.test_journey.serialize()['suspension'],
            True
        )
        self.assertEqual(
            self.test_journey.serialize()['transport_type'],
            'mountain'
        )

    @mock.patch('bike.models.journey.Journey.get_indirect_distance', return_value=1000)
    @mock.patch('bike.models.journey.Journey.duration', 10)
    def test_get_avg_speed(self, mock_get_indirect_distance):
        journey = Journey()
        self.assertEqual(
            journey.get_avg_speed(),
            100
        )

    def test_origin(self):
        self.assertEqual(
            self.test_journey.origin.serialize(),
            {'acc': 1, 'gps': {'lat': 53.3588887, 'lng': -6.2530891, 'elevation': None}, 'time': 0}
        )

    def test_destination(self):
        self.assertEqual(
            self.test_journey.destination.serialize(),
            {'acc': 1, 'gps': {'lat': 53.332599, 'lng': -6.2647978, 'elevation': None}, 'time': 770}
        )

    def test_cull_distance_too_short(self):
        self.test_journey._data = self.test_journey._data[0:3]
        with self.assertRaises(ValueError):
            self.test_journey.cull_distance()

    def test_cull_distance(self):
        # TODO: ensure it doesn't cut too much

        origin_frame = self.test_journey.origin
        destination_frame = self.test_journey.destination

        origin_frames = len(self.test_journey)

        self.test_journey.cull_distance()

        self.assertLess(
            len(self.test_journey),
            origin_frames
        )

        for frame in self.test_journey:
            if frame.distance_from(origin_frame) < EXCLUDE_METRES_BEGIN_AND_END:
                self.fail()

        for frame in self.test_journey:
            if frame.distance_from(destination_frame) < EXCLUDE_METRES_BEGIN_AND_END:
                self.fail()

    def test_cull_time(self):
        # TODO: ensure it doesn't cut too much

        origin_frame = self.test_journey.origin
        destination_frame = self.test_journey.destination

        origin_frames = len(self.test_journey)

        self.test_journey.cull_time(origin_frame.time, destination_frame.time)

        self.assertLess(
            len(self.test_journey),
            origin_frames
        )

        for frame in self.test_journey:
            if frame.time - origin_frame.time < 60 * MINUTES_TO_CUT:
                self.fail()

        for frame in self.test_journey:
            if destination_frame.time - frame.time < 60 * MINUTES_TO_CUT:
                self.fail()

    def test_cull(self):
        # TODO: ensure it doesn't cut too much

        origin_frame = self.test_journey.origin
        destination_frame = self.test_journey.destination

        origin_frames = len(self.test_journey)

        self.test_journey.cull()

        self.assertTrue(self.test_journey.is_culled)

        self.assertLess(
            len(self.test_journey),
            origin_frames
        )

        for frame in self.test_journey:
            if frame.distance_from(origin_frame) < EXCLUDE_METRES_BEGIN_AND_END:
                self.fail()

        for frame in self.test_journey:
            if frame.distance_from(destination_frame) < EXCLUDE_METRES_BEGIN_AND_END:
                self.fail()

        for frame in self.test_journey:
            if frame.time - origin_frame.time < 60 * MINUTES_TO_CUT:
                self.fail()

        for frame in self.test_journey:
            if destination_frame.time - frame.time < 60 * MINUTES_TO_CUT:
                self.fail()

    def test_double_cull(self):
        """A culled journey should fail to cull again"""
        self.test_journey.cull()

        with self.assertRaises(AssertionError):
            self.test_journey.cull()

    def test_duration(self):
        self.assertEqual(
            self.test_journey.duration,
            770
        )

    def test_save_culled(self):
        self.test_journey.is_culled = True
        with self.assertRaises(Exception):
            self.test_journey.save()

    def test_journey_from_file(self):

        journey = Journey()

        for i in range(1000):
            journey.append(
                Frame(
                    0 + i,
                    {'lat': random.random(), 'lng': random.random()},
                    [random.random(), random.random(), random.random()],
                )
            )
        journey.is_culled = False
        journey.save()

        new_journey = Journey.from_file(os.path.join(STAGED_DATA_DIR, str(journey.uuid) + '.json'))

        self.assertEquals(journey.serialize(), new_journey.serialize())

    def test_parse(self):
        self.assertEqual(
            Journey.parse(self.test_journey).serialize(),
            self.test_journey.serialize()
        )

        self.assertEqual(
            Journey.parse(self.test_journey.serialize()).serialize(),
            self.test_journey.serialize()
        )

        with self.assertRaises(NotImplementedError):
            Journey.parse(None)

    def test_plot_route_nothing_fancy(self):
        img_uuid = str(uuid.uuid4())
        fp = os.path.join('/tmp/', img_uuid) + '.jpg'
        self.test_journey.plot_route(
            plot_kwargs={
                'show': False,
                'save': True,
                'filepath': os.path.join('/tmp/', img_uuid) + '.jpg'
            }
        )

        self.assertEqual(
            hashlib.md5(open(fp, 'rb').read()).hexdigest(),
            '33865fc665c74181ae5568db5fdb139f'
        )

    def test_plot_route_use_closest(self):
        img_uuid = str(uuid.uuid4())
        fp = os.path.join('/tmp/', img_uuid) + '.jpg'
        self.test_journey.plot_route(
            use_closest_edge_from_base=True,
            plot_kwargs={
                'show': False,
                'save': True,
                'filepath': os.path.join('/tmp/', img_uuid) + '.jpg'
            }
        )

        self.assertEqual(
            hashlib.md5(open(fp, 'rb').read()).hexdigest(),
            '0f4a71c6015e53bfe45072a6fb2787ba'
        )

    @mock.patch('bike.models.journey.Journey.post_send')
    @mock.patch('requests.post')
    @mock.patch('bike.models.journey.Journey.cull')
    def test_send_ensure_cull(self, cull_mock, post_mock, post_send_mock):
        post_mock.return_value = None
        post_send_mock.return_value = None

        self.test_journey.is_culled = False
        self.test_journey.send()

        self.assertTrue(cull_mock.called)

    @mock.patch('bike.models.journey.DELETE_ON_SEND', True)
    @mock.patch('requests.post')
    @mock.patch('bike.models.journey.Journey.cull')
    def test_send_ensure_post_send_delete(self, cull_mock, post_mock):
        cull_mock.return_value = None
        post_mock.return_value = None

        self.test_journey.save()

        path = os.path.join(STAGED_DATA_DIR, str(self.test_journey.uuid) + '.json')

        self.assertTrue(os.path.exists(path))

        self.test_journey.send()

        self.assertFalse(os.path.exists(path))

    @mock.patch('bike.models.journey.DELETE_ON_SEND', False)
    @mock.patch('requests.post')
    @mock.patch('bike.models.journey.Journey.cull')
    def test_send_ensure_post_send_move(self, cull_mock, post_mock):
        cull_mock.return_value = None
        post_mock.return_value = None

        self.test_journey.save()

        path = os.path.join(STAGED_DATA_DIR, str(self.test_journey.uuid) + '.json')
        sent_path = os.path.join(SENT_DATA_DIR, str(self.test_journey.uuid) + '.json')

        self.assertTrue(os.path.exists(path))
        self.assertFalse(os.path.exists(sent_path))

        self.test_journey.send()

        self.assertFalse(os.path.exists(path))
        self.assertTrue(os.path.exists(sent_path))

    def test_plot_route_use_condition(self):
        # TODO: need to have real data / not random data for the road quality
        pass

    def test_edge_quality_map(self):
        # TODO: need to have real data / not random data for the road quality
        pass

    def test_toggle_gps_acc(self):
        """
        If I don't sort out the phone thing cause I don't want to this should
        make up for it
        """
        test_data = [
            {'time': 0, 'acc': [1, 2, 3], 'gps': {'lat': None, 'lng': None}},
            {'time': 1, 'acc': [1, 2, 3], 'gps': {'lat': None, 'lng': None}},
            {'time': 2, 'acc': [], 'gps': {'lat': 1, 'lng': 2}},
            {'time': 3, 'acc': [1, 2, 3], 'gps': {'lat': None, 'lng': None}},
            {'time': 4, 'acc': [1, 2, 3], 'gps': {'lat': None, 'lng': None}},
            {'time': 5, 'acc': [1, 2, 3], 'gps': {'lat': None, 'lng': None}},
            {'time': 6, 'acc': [1, 2, 3], 'gps': {'lat': None, 'lng': None}},
            {'time': 7, 'acc': [], 'gps': {'lat': 1.1, 'lng': 2.2}},
        ]

        journey = Journey()
        for dp in test_data:
            journey.append(dp)

        self.assertEqual(
            journey.serialize(),
            {
                'uuid': str(journey.uuid),
                'data': [
                    {'gps': {'lat': 1, 'lng': 2, 'elevation': None}, 'acc': None, 'time': 2},
                    {'gps': {'lat': 1, 'lng': 2, 'elevation': None}, 'acc': {'x': 1, 'y': 2, 'z': 3}, 'time': 3},
                    {'gps': {'lat': 1, 'lng': 2, 'elevation': None}, 'acc': {'x': 1, 'y': 2, 'z': 3}, 'time': 4},
                    {'gps': {'lat': 1, 'lng': 2, 'elevation': None}, 'acc': {'x': 1, 'y': 2, 'z': 3}, 'time': 5},
                    {'gps': {'lat': 1, 'lng': 2, 'elevation': None}, 'acc': {'x': 1, 'y': 2, 'z': 3}, 'time': 6},
                    {'gps': {'lat': 1.1, 'lng': 2.2, 'elevation': None}, 'acc': None, 'time': 7}
                ],
                'transport_type': 'mountain',
                'suspension': True,
                'is_culled': False,
                'is_sent': False,
                'direct_distance': 24860.633301979688,
                'indirect_distance': {
                    1: 24860.633301979688,
                    5: 24860.633301979688,
                    10: 0,
                    30: 0
                },
                'data_quality': 0.0,
                'duration': 5,
                'avg_speed': 0.0
            }
        )
