import disnake
from disnake.ext import commands
import aiosqlite
import datetime
import random
from main import embedcolor, errorcolor

class Join(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="확인", emoji="✅", style=disnake.ButtonStyle.green)
    async def click_ok(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        created = ((datetime.datetime.now()) - ctx.author.created_at.replace(tzinfo=None)).days
        if created < 7:
            button.disabled = True
            self.click_cancel.disabled = True
            embed = disnake.Embed(title="취소", description=f"계정생성일이 7일 미만으로 가입이 취소되었습니다\n{7 - created}", color=errorcolor)
            return await ctx.response.edit_message(embed=embed)
        embed = disnake.Embed(title="커미션을 받으시겠습니까?", description="커미션은 봇이 아닌 유저와 작가 디엠에서 일어납니다, 따라서 유저가 친구추가 후 일어납니다", color = embedcolor)
        await ctx.response.edit_message(embed=embed, view=Join2())

    @disnake.ui.button(label="취소", emoji="❌", style=disnake.ButtonStyle.red)
    async def click_cancel(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        button.disabled = True
        self.click_ok.disabled = True
        embed = disnake.Embed(title="취소", description="가입이 취소되었습니다", color=errorcolor)
        await ctx.response.edit_message(embed=embed, view=self)

class Join2(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="네", emoji="✅", style=disnake.ButtonStyle.green)
    async def click_yes(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        gap = datetime.timedelta(hours=9)
        kor_time = datetime.datetime.utcnow() + gap
        today = int(kor_time.strftime("%y%m%d"))
        async with aiosqlite.connect("User.db", isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}") as result:
                data = await result.fetchone()
            if not data is None:
                button.disabled = True
                self.click_no.disabled = True
                embed = disnake.Embed(title="취소", description="이미 가입하셨습니다", color=errorcolor)
                return await ctx.response.edit_message(embed=embed)
            await cursor.execute(f'INSERT INTO user VALUES ({ctx.author.id}, 1, 10, 0, {today})')
        button.disabled = True
        self.click_no.disabled = True
        embed = disnake.Embed(title="가입됐습니다", description="환영합니다 😀", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="아니요", emoji="❌", style=disnake.ButtonStyle.red)
    async def click_no(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        gap = datetime.timedelta(hours=9)
        kor_time = datetime.datetime.utcnow() + gap
        today = int(kor_time.strftime("%y%m%d"))
        async with aiosqlite.connect("User.db", isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}") as result:
                data = await result.fetchone()
            if not data is None:
                button.disabled = True
                self.click_yes.disabled = True
                embed = disnake.Embed(title="취소", description="이미 가입하셨습니다", color=errorcolor)
                return await ctx.response.edit_message(embed=embed)
            await cursor.execute(f'INSERT INTO user VALUES ({ctx.author.id}, 0, 10, 0, {today})')
        button.disabled = True
        self.click_yes.disabled = True
        embed = disnake.Embed(title="가입됐습니다", description="환영합니다 😀", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=self)

class Leave(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="확인", emoji="✅", style=disnake.ButtonStyle.green)
    async def click_ok(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect('User.db', isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}") as result:
                data = await result.fetchone()
            if data is None:
                button.disabled = True
                self.click_cancel.disabled = True
                embed = disnake.Embed(title="오류", description="먼저 가입해주세요", color=errorcolor)
                return await ctx.response.edit_message(embed=embed, view=self)
            await cursor.execute(f"DELETE FROM user WHERE id = {ctx.author.id}")
        async with aiosqlite.connect('Picture.db', isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM picture WHERE author_id = {ctx.author.id}") as result:
                data = await result.fetchall()
            if not data is None:
                await cursor.execute(f"DELETE FROM picture WHERE author_id = {ctx.author.id}") 
        button.disabled = True
        self.click_cancel.disabled = True
        embed = disnake.Embed(title="탈퇴됐습니다", description="안녕히 가세요 😥", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="취소", emoji="❌", style=disnake.ButtonStyle.red)
    async def click_cancel(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        button.disabled = True
        self.click_ok.disabled = True
        embed = disnake.Embed(title="취소", description="탈퇴가 취소되었습니다", color=errorcolor)
        await ctx.response.edit_message(embed=embed, view=self)

class Upload1(disnake.ui.View):
    def __init__(self, picture, title):
        super().__init__(timeout=None)
        self.picture = picture
        self.title = title

    @disnake.ui.button(label="확인", emoji="✅", style=disnake.ButtonStyle.green)
    async def click_ok(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect("Picture.db", isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM picture ORDER BY id DESC") as result:
                data = await result.fetchone()
            if data is None:
                data = [0, "0", 0, 0, 0]
        embed = disnake.Embed(title="이어그리기(리믹스)를 허용하시겠습니까?", description="이어그리기(리믹스) 허용시 다른 유저가 작품을 이어서 그리거나 오마주 할 수 있습니다", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=Upload2(data, self.picture, self.title))
        

    @disnake.ui.button(label="취소", emoji="❌", style=disnake.ButtonStyle.red)
    async def click_cancel(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        self.click_ok.disabled = True
        button.disabled = True
        embed = disnake.Embed(title="취소", description="업로드가 취소되었습니다", color=errorcolor)
        await ctx.response.edit_message(embed=embed, view=self)

class Upload2(disnake.ui.View):
    def __init__(self, data, picture, title):
        super().__init__(timeout=None)
        self.data = data
        self.picture = picture
        self.title = title

    @disnake.ui.button(label="네", emoji="✅", style=disnake.ButtonStyle.green)
    async def click_ok(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect('Picture.db', isolation_level=None) as cursor:
            await cursor.execute(f'INSERT INTO picture VALUES (?, ?, ?, ?, ?, ?, ?)', (self.data[0] + 1, str(self.picture), str(self.title), ctx.author.id, 0, 0, 1))
        button.disabled = True
        self.click_cancel.disabled = True
        embed = disnake.Embed(title="업로드 완료했습니다", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="아니요", emoji="❌", style=disnake.ButtonStyle.red)
    async def click_cancel(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect('Picture.db', isolation_level=None) as cursor:
            await cursor.execute(f'INSERT INTO picture VALUES (?, ?, ?, ?, ?, ?, ?)', (self.data[0] + 1, str(self.picture), str(self.title), ctx.author.id, 0, 0, 0))
        button.disabled = True
        self.click_ok.disabled = True
        embed = disnake.Embed(title="업로드 완료했습니다", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=self)

class Random1(disnake.ui.View):
    def __init__(self, _id, url, author, remix, user, channel):
        super().__init__(timeout=None)
        self._id = _id
        self.url = url
        self.author = author
        self.remix = remix
        self.user = user
        self.channel = channel
        if self.remix == 0:
            self.click_remix.disabled = True
        if author == user.id:
            self.click_remix.disabled = True
            self.click_thumb.disabled = True
        else:
            self.click_delete.disabled = True

    @disnake.ui.button(label="신고", emoji="🚨", style=disnake.ButtonStyle.red)
    async def click_report(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect('User.db', isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}") as result:
                data = await result.fetchone()
            if data is None:
                embed = disnake.Embed(title="오류", description="먼저 가입해주세요", color=errorcolor)
                return await ctx.send(embed=embed, ephemeral=True)
        await ctx.send("디엠을 확인해주세요", ephemeral=True)
        embed = disnake.Embed(title="신고", description="신고 사유를 골라주세요", color=embedcolor)
        await ctx.author.send(embed=embed, view=ReportView(ctx.author, self._id, self.url, self.channel))
        
    @disnake.ui.button(label="이어그리기", emoji="✏️", style=disnake.ButtonStyle.green)
    async def click_remix(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect('User.db', isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}") as result:
                data = await result.fetchone()
            if data is None:
                embed = disnake.Embed(title="오류", description="먼저 가입해주세요", color=errorcolor)
                return await ctx.send(embed=embed, ephemeral=True)

    @disnake.ui.button(label="좋아요", emoji="👍", style=disnake.ButtonStyle.blurple)
    async def click_thumb(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect('User.db', isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM user WHERE id = {ctx.author.id}") as result:
                data = await result.fetchone()
            if data is None:
                embed = disnake.Embed(title="오류", description="먼저 가입해주세요", color=errorcolor)
                return await ctx.send(embed=embed, ephemeral=True)
        async with aiosqlite.connect('Picture.db', isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM thumbs_up WHERE id = {ctx.author.id}") as result:
                data = await result.fetchone()
            if data == None or data[1] == None:
                await cursor.execute(f'INSERT INTO thumbs_up VALUES (?, ?)', (ctx.author.id, ""))
                data = [ctx.author.id, ""]
            if not data[1].find(str(self._id)) == -1:
                data = data[1].replace(f"{str(self._id)},", "")
                await cursor.execute(f"UPDATE thumbs_up SET _id = ? WHERE id = {ctx.author.id}", (data,))
                await cursor.execute(f"UPDATE picture SET thumbs_up = thumbs_up - 1 WHERE id = {self._id}")
                embed = disnake.Embed(title="좋아요가 취소되었습니다", description="좋아요 버튼 다시 클릭으로 취소되었습니다", color=embedcolor)
                await ctx.send(embed=embed)
            else:
                data = data[1] + f"{str(self._id)},"
                await cursor.execute(f"UPDATE thumbs_up SET _id = ? WHERE id = {ctx.author.id}", (data,))
                await cursor.execute(f"UPDATE picture SET thumbs_up = thumbs_up + 1 WHERE id = {self._id}")
                embed = disnake.Embed(title="좋아요가 적용되었습니다", description="좋아요 버튼 클릭으로 적용되었습니다", color=embedcolor)
                await ctx.send(embed=embed)

    @disnake.ui.button(label="삭제", emoji="🗑", style=disnake.ButtonStyle.red, row=1)
    async def click_delete(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        embed = disnake.Embed(title="그림을 삭제하시겠습니까?", description="삭제된 그림은 복구되지 않습니다", color=errorcolor)
        await ctx.send(embed=embed, view=Delete(self._id))

class Report(disnake.ui.Select):
    def __init__(self, user, _id, url, channel):
        self.user = user
        self._id = _id
        self.url = url
        self.channel = channel
        options = [disnake.SelectOption(label="1. 도용 그림", description="개발자에게 친추후 원본 링크 보내주세요"),
        disnake.SelectOption(label="2. 광고 그림", description="커미션 홍보는 제외되요"),
        disnake.SelectOption(label="3. 방송통신심의위원회 SafeNet 15세 기준 위반", description="개발자 판단이긴 하지만 공정하게 판단할거에요")]
        super().__init__(placeholder="신고사유를 골라주세요", min_values=1, max_values=1, options=options)

    async def callback(self, ctx: disnake.MessageInteraction):
        embed = disnake.Embed(title="신고가 접수되었습니다", description="허위신고시 제제를 받을수 있습니다", color=embedcolor)
        self.disabled = True
        await ctx.response.edit_message(embed=embed, view=self.view)
        embed = disnake.Embed(title="신고", description=f"신고자 {self.user}\n그림아이디 {self._id}\n사유 {self.values[0]}", color=errorcolor)
        embed.set_image(url=self.url)
        await self.channel.send(embed=embed)

class ReportView(disnake.ui.View):
    def __init__(self, user, _id, url, channel):
        self.user = user
        self._id =_id
        self.url = url
        self.channel = channel
        super().__init__()
        self.add_item(Report(self.user, self._id, self.url, self.channel))

class Delete(disnake.ui.View):
    def __init__(self, _id):
        self._id = _id
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="네", emoji="✅", style=disnake.ButtonStyle.green)
    async def click_ok(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        async with aiosqlite.connect('Picture.db', isolation_level=None) as cursor:
            await cursor.execute(f"DELETE FROM picture WHERE id = {self._id}")
        button.disabled = True
        self.click_cancel.disabled = True
        embed = disnake.Embed(title="삭제를 완료했습니다", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="아니요", emoji="❌", style=disnake.ButtonStyle.red)
    async def click_cancel(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        button.disabled = True
        self.click_ok.disabled = True
        embed = disnake.Embed(title="삭제를 취소했습니다", color=embedcolor)
        await ctx.response.edit_message(embed=embed, view=self)

class Picture(commands.Cog, name="Picture"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="스케쳐에 가입합니다")
    async def join(self, ctx):
        embed = disnake.Embed(title="가입하시겠습니까?", description="수집되는 정보는 아이디, 가입일, 활동기록입니다", color=embedcolor)
        await ctx.send(embed=embed, view=Join())
    
    @commands.slash_command(description="스케쳐에 탈퇴합니다")
    async def leave(self, ctx):
        embed = disnake.Embed(title="탈퇴하시겠습니까?", description="탈퇴시엔 유저의 모든 정보(그림포함)이 삭제되며, 복구되지 않습니다", color=errorcolor)
        await ctx.send(embed=embed, view=Leave())

    @commands.slash_command(description="그림을 업로드합니다")
    async def upload(self, ctx, picture : str = commands.Param(description="업로드할 그림의 링크"), title : str = commands.Param(description="업로드할 그림의 제목")):
        #/*, –, ‘, “, ?, #, (, ), ;, @, =, *, +, union, select, drop, update, from, where, join, substr, user_tables, user_table_columns, information_schema, sysobject, table_schema, declare, dual
        #정규식으로 검사하기(SQL인젝션)
        if picture.startswith("http") and picture.lower().endswith("png") or picture.lower().endswith("jpg") or picture.lower().endswith("jpeg") or picture.lower().endswith("gif"):
            embed = disnake.Embed(title="그림을 업로드하시겠습니까?", description="규칙을 지켜주세요\n1.도용은 안돼요\n2.광고는 안돼요(커미션 제외)\n3.방송통신심의위원회 SafeNet 기준으로 15세 등급으로 맞춰서 올려주세요", color=embedcolor)
            embed.set_image(url=picture)
            await ctx.send(embed=embed, view=Upload1(picture, title))
        else:
            embed = disnake.Embed(title="오류", description="이미지 링크 형식이나 지원하지 않는 확장자입니다.", color=errorcolor)
            await ctx.send(embed=embed)

    @commands.slash_command(description="무작위로 그림을 불러옵니다")
    async def random(self, ctx):
        async with aiosqlite.connect('Picture.db', isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM picture ORDER BY id DESC") as result:
                data = await result.fetchall()
        one = random.choice(data)
        async with aiosqlite.connect("User.db", isolation_level=None) as cursor:
            async with cursor.execute(f"SELECT * FROM user WHERE id = {one[3]}") as result:
                data = await result.fetchone()
        author = await self.bot.fetch_user(one[3])
        remix = {"0" : "안됨", "1" : "됨"}
        comission = {"0" : "안받음", "1" : "받음"}
        author_fullname = f"  `{str(author)}` 에 친추걸고 연락주세요" if data[1] == 1 else ""
        embed = disnake.Embed(title=one[2], description=f"아이디 : {one[0]}\n작가 : `{author.name}`\n태그 : {one[4]}\n좋아요수 : {one[5]}\n이어그리기 : {remix[str(one[6])]}\n커미션 : {comission[str(data[1])]}{author_fullname}", color=embedcolor)
        embed.set_image(url=one[1])
        await ctx.send(embed=embed, view=Random1(one[0], one[1], one[3], one[6], ctx.author, (await self.bot.fetch_channel(924526922728366090))))

def setup(bot):
    bot.add_cog(Picture(bot))
