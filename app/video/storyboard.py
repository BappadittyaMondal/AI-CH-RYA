"""
AI ĀCHĀRYA — Storyboard & Scene Director Engine (app/video/storyboard.py)

Mission:
Translates any philosophical topic, canonical verse, or historical inquiry into a
production-grade, timed scene-by-scene storyboard for faceless video generation.
Enforces viral retention psychology:
- Hook (0-4s) -> Tension/Pūrvapakṣa (4-15s) -> Primary Evidence (15-40s) -> Synthesis (40-55s).
- Long-form 10-minute documentary act structure (6 acts).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import math


class VideoFormat(str, Enum):
    SHORT_9_16 = "SHORT_9_16 (1080x1920 - YouTube Shorts / Facebook Reels / TikTok)"
    LONG_16_9 = "LONG_16_9 (1920x1080 - YouTube Long Form / Facebook Video)"


class CameraMotion(str, Enum):
    SLOW_ZOOM_IN = "SLOW_ZOOM_IN"
    SLOW_ZOOM_OUT = "SLOW_ZOOM_OUT"
    PAN_LEFT_TO_RIGHT = "PAN_LEFT_TO_RIGHT"
    SUBTLE_PULSE = "SUBTLE_PULSE"


@dataclass(frozen=True)
class SceneBeat:
    scene_number: int
    start_sec: float
    end_sec: float
    duration_sec: float
    narration_text: str
    visual_theme: str
    visual_prompt: str
    on_screen_devanagari: str
    on_screen_iast: str
    sfx_cue: str
    motion_type: CameraMotion


@dataclass(frozen=True)
class VideoStoryboard:
    project_id: str
    topic: str
    video_format: VideoFormat
    language: str
    total_duration_sec: float
    target_platforms: List[str]
    seo_title: str
    seo_description: str
    seo_tags: List[str]
    scenes: List[SceneBeat]


class VideoStoryboardDirector:
    """
    Directs scriptwriting, pacing, and visual prompts for faceless documentary production.
    """

    @classmethod
    def create_storyboard(
        cls,
        topic: str,
        video_format: VideoFormat = VideoFormat.SHORT_9_16,
        language: str = "en",
        target_duration: Optional[float] = None
    ) -> VideoStoryboard:
        """
        Generates an end-to-end storyboard manifest tailored to format and platform constraints.
        """
        top_lower = topic.lower().strip()
        is_short = (video_format == VideoFormat.SHORT_9_16)
        
        # 1. Determine Narrative Script & Scene Beats
        if "bg 2.47" in top_lower or "karma" in top_lower or "right to work" in top_lower:
            scenes = cls._build_bg_2_47_storyboard(is_short, language)
            title = "The Secret of Karma Yoga: Bhagavad Gītā 2.47 Decoded"
            desc = "Understand the true psychological freedom of working without anxiety of results per Śrī Kṛṣṇa in Bhagavad Gītā 2.47."
            tags = ["BhagavadGita", "KarmaYoga", "SanatanaDharma", "Mindset", "Philosophy"]
        elif "purusha" in top_lower or "puruṣa" in top_lower or "organicism" in top_lower or "caste" in top_lower:
            scenes = cls._build_purusha_sukta_storyboard(is_short, language)
            title = "Puruṣa Sūkta: The Cosmic Organism That Shatters Colonial Myths"
            desc = "How Ṛgveda 10.90 reveals the sacred cosmic body where the Earth emanates from the feet of the Divine."
            tags = ["Rigveda", "PurushaSukta", "Vedas", "AncientIndia", "Dharma"]
        elif "code" in top_lower or "rishi" in top_lower or "secret" in top_lower:
            scenes = cls._build_rishi_code_storyboard(is_short, language)
            title = "Was Every Word Written by the Rishis a Code? The Real Science"
            desc = "Deconstructing the Katapayādi number system, Pāṇinian grammar algorithms, and Vedic acoustic error checks."
            tags = ["AncientScience", "Sanskrit", "Panini", "Katapayadi", "VedicMath"]
        elif "cyber" in top_lower or "arrest" in top_lower or "scam" in top_lower:
            scenes = cls._build_cyber_defense_storyboard(is_short, language)
            title = "Digital Arrest Scam: Ancient Chanakya Defense & Helpline 1930"
            desc = "How fraudsters exploit fear and unearned greed, and how to stop them using Arthaśāstra principles."
            tags = ["CyberSecurity", "DigitalArrest", "ScamAlert", "Helpline1930", "Chanakya"]
        else:
            scenes = cls._build_generic_civilization_storyboard(topic, is_short, language)
            title = f"Unveiling the Hidden Truth of {topic.title()}"
            desc = f"A rigorous forensic and civilizational analysis of {topic} grounded in primary evidence."
            tags = ["SanatanaDharma", "Civilization", "History", "Wisdom", "DeepTech"]

        total_dur = sum(s.duration_sec for s in scenes)
        proj_id = f"PROJ_{abs(hash(topic)) % 100000:05d}_{'SHORT' if is_short else 'LONG'}"
        platforms = ["YouTube Shorts", "Facebook Reels", "Instagram Reels"] if is_short else ["YouTube", "Facebook Video"]

        return VideoStoryboard(
            project_id=proj_id,
            topic=topic,
            video_format=video_format,
            language=language,
            total_duration_sec=round(total_dur, 1),
            target_platforms=platforms,
            seo_title=title,
            seo_description=desc,
            seo_tags=tags,
            scenes=scenes
        )

    @classmethod
    def _build_bg_2_47_storyboard(cls, is_short: bool, lang: str) -> List[SceneBeat]:
        if is_short:
            return [
                SceneBeat(
                    scene_number=1, start_sec=0.0, end_sec=5.0, duration_sec=5.0,
                    narration_text="You have a right to action, but never to its results.",
                    visual_theme="Sacred Battlefield Antiquity",
                    visual_prompt="Cinematic close-up of an ancient Bronze Age warrior armor resting on stone altar, dramatic Rembrandt lighting, chiaroscuro shadows, dust motes in sunlight, 8k documentary, no human face",
                    on_screen_devanagari="कर्मण्येवाधिकारस्ते",
                    on_screen_iast="karmaṇy evādhikāras te",
                    sfx_cue="DEEP_WAR_HORN_CHIME",
                    motion_type=CameraMotion.SLOW_ZOOM_IN
                ),
                SceneBeat(
                    scene_number=2, start_sec=5.0, end_sec=18.0, duration_sec=13.0,
                    narration_text="In Bhagavad Gītā 2.47, Śrī Kṛṣṇa delivers the ultimate cure for performance anxiety: when you obsess over the outcome, you poison your execution.",
                    visual_theme="Parchment Manuscript Macro",
                    visual_prompt="Macro photorealistic shot of an authentic birch bark manuscript with radiant gold Devanagari ink, warm temple oil lamp glow in background, museum display, 8k",
                    on_screen_devanagari="मा फलेषु कदाचन",
                    on_screen_iast="mā phaleṣu kadācana",
                    sfx_cue="SUBTLE_TIBETAN_BOWL",
                    motion_type=CameraMotion.PAN_LEFT_TO_RIGHT
                ),
                SceneBeat(
                    scene_number=3, start_sec=18.0, end_sec=36.0, duration_sec=18.0,
                    narration_text="Pāṇinian grammar defines adhikāra as your sphere of jurisdiction. You control effort, focus, and integrity—the universe controls the fruit.",
                    visual_theme="Cosmic Sacred Architecture",
                    visual_prompt="Monolithic granite temple sanctum illuminated by single vertical sunbeam, ancient fractal carvings of sacred geometry, misty atmosphere, majestic silence, 8k",
                    on_screen_devanagari="मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि",
                    on_screen_iast="mā karmaphalahetur bhūḥ",
                    sfx_cue="TEMPLE_BELL_CHIME",
                    motion_type=CameraMotion.SLOW_ZOOM_OUT
                ),
                SceneBeat(
                    scene_number=4, start_sec=36.0, end_sec=50.0, duration_sec=14.0,
                    narration_text="Act with 100 percent intensity, detach from the outcome, and achieve absolute psychological freedom. This is authentic Karma Yoga.",
                    visual_theme="Sunrise Horizon Solitude",
                    visual_prompt="Silhouette of an empty mountain summit at dawn, golden sunrise illuminating Himalayan mist, deep contemplative tranquility, majestic, photorealistic",
                    on_screen_devanagari="योगस्थः कुरु कर्माणि",
                    on_screen_iast="yogasthaḥ kuru karmāṇi",
                    sfx_cue="RESONANT_GONG_FADE",
                    motion_type=CameraMotion.SLOW_ZOOM_IN
                )
            ]
        else:
            # Long-form 10-minute documentary (demonstration acts)
            beats = []
            dur_per_beat = 60.0
            for i in range(1, 11):
                beats.append(
                    SceneBeat(
                        scene_number=i,
                        start_sec=(i - 1) * dur_per_beat,
                        end_sec=i * dur_per_beat,
                        duration_sec=dur_per_beat,
                        narration_text=f"Act {i}: Exploring the profound dimensions of Karma Yoga, epistemic detachment, and cognitive mastery in Bhagavad Gītā Chapter 2.",
                        visual_theme=f"Documentary Act {i} Sacred Visual",
                        visual_prompt=f"Cinematic historical documentary landscape scene {i}, ancient stone architecture, dusk sky, photorealistic 8k, no human face",
                        on_screen_devanagari="कर्मण्येवाधिकारस्ते",
                        on_screen_iast="karmaṇy evādhikāras te",
                        sfx_cue="SUBTLE_DRONE_TRANSITION",
                        motion_type=CameraMotion.SLOW_ZOOM_IN
                    )
                )
            return beats

    @classmethod
    def _build_purusha_sukta_storyboard(cls, is_short: bool, lang: str) -> List[SceneBeat]:
        if is_short:
            return [
                SceneBeat(
                    scene_number=1, start_sec=0.0, end_sec=6.0, duration_sec=6.0,
                    narration_text="Did the ancient Vedas really create an oppressive hierarchy? The original Sanskrit text says the exact opposite.",
                    visual_theme="Cosmic Purusha Nebula",
                    visual_prompt="Cosmic golden nebula swirling in deep space resembling a vast interconnected universal organism, stellar dust, celestial harmony, 8k cinematic",
                    on_screen_devanagari="सहस्रशीर्षा पुरुषः",
                    on_screen_iast="sahasraśīrṣā puruṣaḥ",
                    sfx_cue="DEEP_SPACE_DRONE",
                    motion_type=CameraMotion.SLOW_ZOOM_IN
                ),
                SceneBeat(
                    scene_number=2, start_sec=6.0, end_sec=22.0, duration_sec=16.0,
                    narration_text="In Ṛgveda 10.90, the Puruṣa Sūkta models society not as a ladder, but as a single living cosmic body where every limb is divine.",
                    visual_theme="Sacred Macrocosm Alignment",
                    visual_prompt="Ancient temple pillars carved with sacred tree of life motifs, roots connecting to glowing earth, volumetric golden fog, awe-inspiring, 8k",
                    on_screen_devanagari="ब्राह्मणोऽस्य मुखमासीद् बाहू राजन्यः कृतः",
                    on_screen_iast="mukham āsīd bāhū rājanyaḥ",
                    sfx_cue="TEMPLE_BELL_CHIME",
                    motion_type=CameraMotion.PAN_LEFT_TO_RIGHT
                ),
                SceneBeat(
                    scene_number=3, start_sec=22.0, end_sec=38.0, duration_sec=16.0,
                    narration_text="And in verse 14, it states: from His feet, the sacred Earth was born! In Vedic culture, the Earth is worshipped as the Supreme Mother.",
                    visual_theme="Sacred Earth Pratiṣṭhā",
                    visual_prompt="Cinematic ground-level shot of fertile green soil with blooming lotus flowers, early morning dew drops catching sunlight, sacred reverence, 8k",
                    on_screen_devanagari="पद्भ्यां भूमिर्दिशः श्रोत्रात्",
                    on_screen_iast="padbhyāṃ bhūmir diśaḥ śrotrāt",
                    sfx_cue="SUBTLE_TIBETAN_BOWL",
                    motion_type=CameraMotion.SLOW_ZOOM_OUT
                ),
                SceneBeat(
                    scene_number=4, start_sec=38.0, end_sec=52.0, duration_sec=14.0,
                    narration_text="The feet are the locus of sacred stability (Pratiṣṭhā). The head cannot live without the feet. Unity was sung, not division.",
                    visual_theme="Harmonic Cosmic Light",
                    visual_prompt="Ancient monolithic stone mandala reflecting starlight on pristine lake, serene night sky, spiritual unity, photorealistic 8k",
                    on_screen_devanagari="तथा लोकाँ अकल्पयन्",
                    on_screen_iast="tathā lokāṁ akalpayan",
                    sfx_cue="RESONANT_GONG_FADE",
                    motion_type=CameraMotion.SLOW_ZOOM_IN
                )
            ]
        else:
            # 6-Act 10-Minute Long-Form Documentary Structure
            act_dur = 80.0
            act_titles = [
                ("सहस्रशीर्षा पुरुषः", "sahasraśīrṣā puruṣaḥ", "Act 1: The Cosmic Vision of Ṛgveda 10.90", "Cosmic Purusha Nebula"),
                ("ब्राह्मणोऽस्य मुखमासीत्", "brāhmaṇo 'sya mukham āsīt", "Act 2: The Organic Cosmic Body: Functional Interdependence", "Sacred Macrocosm Alignment"),
                ("पद्भ्यां भूमिर्दिशः श्रोत्रात्", "padbhyāṃ bhūmir diśaḥ śrotrāt", "Act 3: The Sanctity of the Earth and the Feet (Pratiṣṭhā)", "Sacred Earth Pratiṣṭhā"),
                ("यज्ञेन यज्ञमयजन्त देवाः", "yajñena yajñam ayajanta devāḥ", "Act 4: Cosmic Sacrifice and Ecological Equilibrium", "Cosmic Altar Resonance"),
                ("तस्माद्यज्ञात्सर्वहुतः", "tasmād yajñāt sarvahutaḥ", "Act 5: Deconstructing 19th-Century Colonial Degradation", "Historical Epistemic Archive"),
                ("वेदाहमेतं पुरुषं महान्तम्", "vedāham etaṃ puruṣaṃ mahāntam", "Act 6: Transcending Division: The Sun Beyond Darkness", "Harmonic Cosmic Light")
            ]
            acts: List[SceneBeat] = []
            for idx, (deva, iast, narration_topic, theme) in enumerate(act_titles, start=1):
                acts.append(
                    SceneBeat(
                        scene_number=idx,
                        start_sec=(idx - 1) * act_dur,
                        end_sec=idx * act_dur,
                        duration_sec=act_dur,
                        narration_text=f"{narration_topic}. Rigorous textual analysis of the Sanskrit root reveals an indivisible living cosmic organism, refuting colonial hierarchical models.",
                        visual_theme=theme,
                        visual_prompt=f"Cinematic historical documentary landscape for {narration_topic}, atmospheric volumetric haze, 8k photorealistic, no human face",
                        on_screen_devanagari=deva,
                        on_screen_iast=iast,
                        sfx_cue="TEMPLE_BELL_CHIME",
                        motion_type=CameraMotion.SLOW_ZOOM_IN
                    )
                )
            return acts

    @classmethod
    def _build_rishi_code_storyboard(cls, is_short: bool, lang: str) -> List[SceneBeat]:
        return [
            SceneBeat(
                scene_number=1, start_sec=0.0, end_sec=5.0, duration_sec=5.0,
                narration_text="Was every word written by ancient Indian sages an encrypted code? Here is the real science.",
                visual_theme="Ancient Sanskrit Cryptography",
                visual_prompt="Glowing Sanskrit Devanagari characters floating over an ancient stone astrolabe, illuminated by candle flame, dark academia aesthetic, 8k",
                on_screen_devanagari="शब्दो ब्रह्म",
                on_screen_iast="śabdo brahma",
                sfx_cue="MYSTERIOUS_WHOOSH",
                motion_type=CameraMotion.SLOW_ZOOM_IN
            ),
            SceneBeat(
                scene_number=2, start_sec=5.0, end_sec=20.0, duration_sec=15.0,
                narration_text="Ancient mathematicians like Āryabhaṭa genuinely used the Katapayādi alphanumeric cipher to encode the value of Pi and planetary distances into poetic verses.",
                visual_theme="Astrolabe & Celestial Geometry",
                visual_prompt="Intricate antique brass astronomical instrument measuring planetary conjunctions against star charts, detailed brass gears, 8k",
                on_screen_devanagari="कटपयादि सङ्ख्या",
                on_screen_iast="ka-ṭa-pa-yādi saṅkhyā",
                sfx_cue="BRASS_GEAR_CHIME",
                motion_type=CameraMotion.PAN_LEFT_TO_RIGHT
            ),
            SceneBeat(
                scene_number=3, start_sec=20.0, end_sec=36.0, duration_sec=16.0,
                narration_text="And Pāṇini created the world's first recursive generative grammar—the foundational ancestor of modern computer compiler design.",
                visual_theme="Algorithmic Lattice Work",
                visual_prompt="Sanskrit palm-leaf manuscript illuminated by fiber-optic blue-and-gold light trails showing recursive algorithmic branching, 8k",
                on_screen_devanagari="अष्टाध्यायी सूत्र",
                on_screen_iast="aṣṭādhyāyī sūtra",
                sfx_cue="DATA_STREAM_CHIME",
                motion_type=CameraMotion.SLOW_ZOOM_OUT
            ),
            SceneBeat(
                scene_number=4, start_sec=36.0, end_sec=52.0, duration_sec=16.0,
                narration_text="The sages were not hiding sci-fi secret codes; they engineered mathematical, acoustic, and linguistic perfection for human consciousness.",
                visual_theme="Golden Temple Twilight",
                visual_prompt="Golden temple reflection in tranquil river at twilight, soft spiritual radiance, majestic architectural symmetry, 8k cinematic",
                on_screen_devanagari="सत्यं ज्ञानमनन्तं ब्रह्म",
                on_screen_iast="satyaṃ jñānam anantaṃ brahma",
                sfx_cue="RESONANT_GONG_FADE",
                motion_type=CameraMotion.SLOW_ZOOM_IN
            )
        ]

    @classmethod
    def _build_cyber_defense_storyboard(cls, is_short: bool, lang: str) -> List[SceneBeat]:
        return [
            SceneBeat(
                scene_number=1, start_sec=0.0, end_sec=5.0, duration_sec=5.0,
                narration_text="If you get a Skype call claiming you are under Digital Arrest by the police—HANG UP IMMEDIATELY.",
                visual_theme="Digital Threat Matrix",
                visual_prompt="Dark modern room with glowing computer monitor displaying red warning alert shield, dramatic high-contrast lighting, 8k cinematic",
                on_screen_devanagari="भय-कूट निरोध",
                on_screen_iast="bhaya-kūṭa nirodha",
                sfx_cue="ALARM_PULSE_CHIME",
                motion_type=CameraMotion.SLOW_ZOOM_IN
            ),
            SceneBeat(
                scene_number=2, start_sec=5.0, end_sec=18.0, duration_sec=13.0,
                narration_text="There is no law called Digital Arrest in India. Law enforcement never summons citizens or demands money over video calls.",
                visual_theme="Legal Seal & Shield",
                visual_prompt="Golden scales of justice resting beside an ancient Ashoka pillar emblem, majestic legal integrity, 8k",
                on_screen_devanagari="सत्यमेव जयते",
                on_screen_iast="satyameva jayate",
                sfx_cue="COURT_GAVEL_CHIME",
                motion_type=CameraMotion.PAN_LEFT_TO_RIGHT
            ),
            SceneBeat(
                scene_number=3, start_sec=18.0, end_sec=32.0, duration_sec=14.0,
                narration_text="Extortionists exploit fear (Bhaya). Take a deep breath, observe their tricks with detached awareness, and refuse to wire funds.",
                visual_theme="Charioteer Mind Control",
                visual_prompt="Ancient Vedic war chariot with disciplined white horses standing poised under control of steady charioteer, Katha Upanishad allegory, 8k",
                on_screen_devanagari="आत्मानं रथिनं विद्धि",
                on_screen_iast="ātmānaṃ rathinaṃ viddhi",
                sfx_cue="SUBTLE_TIBETAN_BOWL",
                motion_type=CameraMotion.SLOW_ZOOM_OUT
            ),
            SceneBeat(
                scene_number=4, start_sec=32.0, end_sec=48.0, duration_sec=16.0,
                narration_text="Dial National Cyber Crime Helpline 1930 immediately or visit cybercrime.gov.in. Protect your elders and share this truth.",
                visual_theme="National Cybersecurity Shield",
                visual_prompt="Glowing national cyber defense shield emblem with telephone hotline icon 1930 radiating emerald security light, 8k",
                on_screen_devanagari="हेल्पलाइन १९३०",
                on_screen_iast="helpline 1930",
                sfx_cue="SECURITY_CONFIRM_CHIME",
                motion_type=CameraMotion.SLOW_ZOOM_IN
            )
        ]

    @classmethod
    def _build_generic_civilization_storyboard(cls, topic: str, is_short: bool, lang: str) -> List[SceneBeat]:
        return [
            SceneBeat(
                scene_number=1, start_sec=0.0, end_sec=6.0, duration_sec=6.0,
                narration_text=f"What is the deeper truth behind {topic}? Look past the surface illusions.",
                visual_theme="Ancient Archaeological Gateway",
                visual_prompt="Massive ancient stone gateway adorned with intricate Indic bas-reliefs, warm dawn sunbeams piercing morning mist, 8k cinematic",
                on_screen_devanagari="सत्यं वद धर्मं चर",
                on_screen_iast="satyaṃ vada dharmaṃ cara",
                sfx_cue="DEEP_WAR_HORN_CHIME",
                motion_type=CameraMotion.SLOW_ZOOM_IN
            ),
            SceneBeat(
                scene_number=2, start_sec=6.0, end_sec=22.0, duration_sec=16.0,
                narration_text=f"When we analyze {topic} through primary manuscripts, material epigraphy, and scientific logic, false narratives dissolve.",
                visual_theme="Lithic Inscription Detail",
                visual_prompt="Macro close-up of ancient Brahmi and Sanskrit rock edict carved in weather-beaten granite cliff, tactile archaeological depth, 8k",
                on_screen_devanagari="शिलालेख प्रमाण",
                on_screen_iast="śilālekha pramāṇa",
                sfx_cue="TEMPLE_BELL_CHIME",
                motion_type=CameraMotion.PAN_LEFT_TO_RIGHT
            ),
            SceneBeat(
                scene_number=3, start_sec=22.0, end_sec=38.0, duration_sec=16.0,
                narration_text="Authentic civilizational knowledge unites rigorous empirical science with timeless inner realization. The evidence speaks for itself.",
                visual_theme="Sacred Water & Stone",
                visual_prompt="Ancient river ghat steps descending into glistening sacred water at sunset, oil lamps floating, peaceful timeless serenity, 8k",
                on_screen_devanagari="प्रत्यक्ष प्रमाण",
                on_screen_iast="pratyakṣa pramāṇa",
                sfx_cue="SUBTLE_TIBETAN_BOWL",
                motion_type=CameraMotion.SLOW_ZOOM_OUT
            ),
            SceneBeat(
                scene_number=4, start_sec=38.0, end_sec=52.0, duration_sec=14.0,
                narration_text="Dharma is not dogma; it is cosmic order and conscious living. Stay grounded, stay sovereign, and seek the truth.",
                visual_theme="Ascending Light Sanctum",
                visual_prompt="Silhouetted temple shikara against a star-studded galaxy, cosmic wonder, golden illumination from inner sanctum, 8k",
                on_screen_devanagari="धर्मो रक्षति रक्षितः",
                on_screen_iast="dharmo rakṣati rakṣitaḥ",
                sfx_cue="RESONANT_GONG_FADE",
                motion_type=CameraMotion.SLOW_ZOOM_IN
            )
        ]
