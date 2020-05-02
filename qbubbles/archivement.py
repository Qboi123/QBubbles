from time import sleep


class Achievement:
    def __init__(self):
        pass

    def earned_event_int(self, root, canvas, config, stats, stat_id, max_value, achievements, achiev_name):
        earned = False
        while root.winfo_exists() or earned:
            if stats[stat_id] >= max_value:
                earned = True
                self.earn_achievement(canvas, config, achievements, achiev_name)
            sleep(0.25)

    @staticmethod
    def earn_achievement(canvas, config, achievements, achiev_name):
        # noinspection PyUnusedLocal
        a_id = canvas.create_image(config["width"]-300, 150, image=achievements[achiev_name]["image"])
        achievements[achiev_name]["status"] = False
