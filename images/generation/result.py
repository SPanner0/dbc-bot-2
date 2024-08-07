from typing import Union
from PIL.Image import Resampling
from pydantic import BaseModel
from .model import Background, Component, BaseImage, Player
import base64


class RequestResult(BaseModel):
    winner: Player
    loser: Player

    async def respond(self) -> Union[str, Exception]:
        image = await Result(self.winner, self.loser)
        if image.error:
            return image.error
        image.preset()
        image.build()
        encode = base64.b64encode(image.bytes()).decode("utf-8")
        return encode


class Result(BaseImage):
    async def __init__(self, winner: Player, loser: Player):
        bg, self.error = self.asset.get_image("Winner_Loser_clean.png")
        await super().__init__(bg=Background(None, None, bg, "Result"))
        self.winner: Player = winner
        self.loser: Player = loser
        self.pi1, self.error = await self.asset.icon(self.winner.icon)
        self.pi2, self.error = await self.asset.icon(self.loser.icon)

    def preset(self):
        ICON_SIZE = (275, 275)
        icon1 = Component(
            img=self.pi1.resize(size=ICON_SIZE, resample=Resampling.NEAREST),
            pos=(175, 175),
            name="Icon1",
        )
        icon2 = Component(
            img=self.pi2.resize(size=ICON_SIZE, resample=Resampling.NEAREST).convert(
                mode="L"
            ),
            pos=(830, 175),
            name="Icon2",
        )
        self.write(
            text=self.winner.discord_name,
            textbox_pos=((125, 460), (500, 530)),
            align="center",
            color=(255, 255, 255),
        )
        self.write(
            text=self.loser.discord_name,
            textbox_pos=((780, 460), (1155, 530)),
            align="center",
            color=(255, 255, 255),
        )
        self.components.extend([icon1, icon2])
