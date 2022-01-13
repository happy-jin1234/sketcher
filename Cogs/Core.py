import disnake
from disnake.ext import commands
from main import embedcolor, errorcolor
import platform


class Core(commands.Cog, name="Core"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="개발자를 표시합니다")
    async def hellothisisverification(self, ctx):
        jin = await self.bot.fetch_user(671231351013376015)
        embed = disnake.Embed(description=f"개발자는 {jin}(671231351013376015) 입니다", color=embedcolor)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @commands.slash_command(description="봇의 메세지 지연시간을 표시합니다")
    async def ping(self, ctx):
        embed = disnake.Embed(title="<a:infloading:921601343154716705> 핑 측정중", color=embedcolor)
        await ctx.send(embed=embed)
        msg = await ctx.original_message()
        pings = round(self.bot.latency * 1000)
        latency = int((msg.created_at - ctx.created_at).microseconds/1000)
        embed = disnake.Embed(
            title="핑",
            description=f"디스코드 레이턴시 : {pings} ms\n메세지 지연시간 : {latency}ms",
            color=embedcolor,
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar)
        await msg.edit(embed=embed)

    @commands.slash_command(description="봇의 정보를 표시합니다")
    async def info(self, ctx):
        embed = disnake.Embed(title="봇 정보", color=embedcolor)
        embed.add_field(name="이름", value=self.bot.user, inline=False)
        embed.add_field(name="별명", value=self.bot.user.display_name)
        embed.add_field(
            name="가입일",
            value=f"<t:{int(self.bot.user.created_at.timestamp())}> (<t:{int(self.bot.user.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.add_field(name="아이디", value=self.bot.user.id, inline=False)
        embed.add_field(name="운영체제", value=platform.system())
        embed.add_field(name="운영체제 버젼", value=platform.version())
        embed.add_field(name="프로세스 아키텍쳐", value=platform.machine())
        embed.add_field(name="서버 수", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="유저 수", value=len(self.bot.users))
        embed.add_field(name="개발자", value=str(await self.bot.fetch_user(671231351013376015)))
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)


    @commands.slash_command(description="도움말을 표시합니다")
    async def help(self, ctx):
        embed = disnake.Embed(
            title="도움말", description="안녕하세요 스케쳐입니다.\n스케쳐의 기능은 본인이 그린 작품을 자랑할수 있고, 또 남이 그린 작품도 감상하실 수 있습니다.", color=embedcolor
        )            
        cog_list = [
            "Core",
            "Picture"
        ]
        for x in cog_list:
            cog_data = self.bot.get_cog(x)
            command_list = cog_data.get_slash_commands()
            embed.add_field(
                name=x, value=" ".join([f"`/{c.name}`" for c in command_list])
            )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Core(bot))
