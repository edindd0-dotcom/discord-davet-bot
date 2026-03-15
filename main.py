import discord
import os
from discord.ext import commands

# Ayarlar - DISCORD_TOKEN'ı Environment Variables kısmına eklemeyi unutma!
TOKEN = os.getenv('DISCORD_TOKEN')
HEDEF_ID = 1190624788159410256
GEREKEN_DAVET = 3

class DavetButonu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ödülü Al", style=discord.ButtonStyle.success, custom_id="odul_al", emoji="🎁")
    async def button_callback(self, interaction: discord.Interaction):
        # Davetleri kontrol etmek için etkileşimi beklemeye alıyoruz
        await interaction.response.defer(ephemeral=True)
        
        invites = await interaction.guild.invites()
        # Butona basan kişinin toplam davet sayısını hesapla
        user_invites = sum(i.uses for i in invites if i.inviter and i.inviter.id == interaction.user.id)
        
        if user_invites >= GEREKEN_DAVET:
            await interaction.followup.send(
                content=f"✅ **Tebrikler!** Toplam **{user_invites}** davetin var.\n"
                        f"Ödülünü almak için <@{HEDEF_ID}> kişisine DM üzerinden **2xNitro** yazman yeterli!",
                ephemeral=True
            )
        else:
            eksik = GEREKEN_DAVET - user_invites
            await interaction.followup.send(
                content=f"❌ **Maalesef davet sayın yetersiz.**\n"
                        f"Şu an **{user_invites}** davetin var. Ödülü alabilmek için **{eksik}** tane daha davet yapman gerekiyor!",
                ephemeral=True
            )

class MyBot(commands.Bot):
    def __init__(self):
        # Komut ön ekini . (nokta) olarak ayarladık
        intents = discord.Intents.default()
        intents.members = True
        intents.invites = True
        intents.message_content = True
        super().__init__(command_prefix=".", intents=intents)

    async def setup_hook(self):
        # Bot kapansa bile butonun çalışmaya devam etmesi için view'ı kaydediyoruz
        self.add_view(DavetButonu())

bot = MyBot()

@bot.command(name="event")
@commands.has_permissions(administrator=True) # Sadece adminler bu yazıyı atabilir
async def event(ctx):
    embed = discord.Embed(
        title="🎁 Davet Ödülü Sistemi",
        description=f"Sunucumuza **{GEREKEN_DAVET} davet** getiren herkese Nitro hediye ediyoruz!\n\n"
                    "Alttaki butona basarak davet sayını kontrol edebilir ve ödülü isteyebilirsin.",
        color=discord.Color.green()
    )
    embed.set_footer(text="Gerçek valla, hemen arkadaşını çağır!")
    
    await ctx.send(embed=embed, view=DavetButonu())

# Botu çalıştır
if TOKEN:
    bot.run(TOKEN)
else:
    print("Hata: DISCORD_TOKEN bulunamadı!")
