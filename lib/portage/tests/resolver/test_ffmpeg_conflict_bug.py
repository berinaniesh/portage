# Copyright 2023 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

from portage.tests import TestCase
from portage.tests.resolver.ResolverPlayground import (
    ResolverPlayground,
    ResolverPlaygroundTestCase,
)


class FfmpegConflictTestCase(TestCase):
    def test_ffmpeg_conflict(self):
        ebuilds = {
            "media-plugins/vdr-xineliboutput-1.1.0": {
                "EAPI": "5",
                "DEPEND": " >=media-video/vdr-1.6.0 >=media-libs/xine-lib-1.2 ",
                "SLOT": "0",
            },
            "media-plugins/vdr-xineliboutput2-1.1.0": {
                "EAPI": "5",
                "DEPEND": " >=media-video/vdr-1.6.0 >=media-libs/xine-lib2-1.2 ",
                "SLOT": "0",
            },
            "media-video/vdr-2.0.6": {
                "EAPI": "5",
                "DEPEND": "virtual/ffmpeg",
                "SLOT": "0",
            },
            "media-libs/xine-lib-1.2.6": {
                "EAPI": "5",
                "DEPEND": "|| ( media-video/ffmpeg media-libs/libpostproc <media-video/libav-0.8.2-r1 ) virtual/ffmpeg",
                "SLOT": "0",
            },
            "media-libs/xine-lib2-1.2.6": {
                "EAPI": "5",
                "DEPEND": "media-video/libav",
                "SLOT": "0",
            },
            "virtual/ffmpeg-9.0": {
                "EAPI": "5",
                "DEPEND": "|| ( >=media-video/libav-9 >=media-video/ffmpeg-1.0 )",
                 "SLOT": "0",
            },
            "media-libs/libpostproc-10.20140517": {
                "EAPI": "5",
                "DEPEND": ">=virtual/ffmpeg-0.10.2-r2",
                 "SLOT": "0",
            },
            "media-video/ffmpeg-2.4.3": {
                "EAPI": "5",
                "DEPEND": "",
                "SLOT": "0",
            },
            "media-video/libav-9.0.1": {
                "EAPI": "5",
                "DEPEND": "",
                "SLOT": "0",
            },
        }

        installed = {}
        world = []

        test_cases = (
            ResolverPlaygroundTestCase(
                ["media-plugins/vdr-xineliboutput"],
                options={"--verbose": True, "update": True, "--deep": True},
                success=True,
                ambiguous_merge_order=True,
                merge_order_assertions=(
                    (
                        "media-video/ffmpeg-2.4.3",
                        "media-libs/xine-lib-1.2.6",
                    ),
                ),
                mergelist=[
                    "media-video/ffmpeg-2.4.3",
                    "media-libs/xine-lib-1.2.6",
                    "virtual/ffmpeg-9.0",
                    "media-video/vdr-2.0.6",
                    "media-plugins/vdr-xineliboutput-1.1.0",
                ],
            ),
            ResolverPlaygroundTestCase(
                ["media-plugins/vdr-xineliboutput2"],
                options={"--verbose": True, "update": True, "--deep": True},
                success=True,
                ambiguous_merge_order=True,
                merge_order_assertions=(
                    (
                        "media-video/libav-9.0.1",
                        "media-libs/xine-lib2-1.2.6",
                    ),
                ),
                mergelist=[
                    "media-video/libav-9.0.1",
                    "media-libs/xine-lib2-1.2.6",
                    "virtual/ffmpeg-9.0",
                    "media-video/vdr-2.0.6",
                    "media-plugins/vdr-xineliboutput2-1.1.0",
                ],
            ),
        )

        playground = ResolverPlayground(
            ebuilds=ebuilds,
            installed=installed,
            world=world,
        )
        try:
            for test_case in test_cases:
                playground.run_TestCase(test_case)
                self.assertEqual(test_case.test_success, True, test_case.fail_msg)
        finally:
            playground.cleanup()

