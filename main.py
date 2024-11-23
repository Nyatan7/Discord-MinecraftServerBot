import discord
import os
import os.path
from dotenv import load_dotenv
import subprocess
import time
import glob
from discord.ext import commands

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
bot.remove_command("help")



# 環境変数の読み込み

load_dotenv(".env")

f_name        = os.getenv("f_name")
maxMemory     = os.getenv("maxMemory")
minMemory     = os.getenv("minMemory")
global_ip     = os.getenv("global_ip")
port_java     = os.getenv("port_java")
port_be       = os.getenv("port_be")
port_livekit  = os.getenv("port_livekit")
port_bluemap  = os.getenv("port_bluemap")
plugin        = os.getenv("plugin")
world_path    = os.getenv("world_path")
nether_path   = os.getenv("nether_path")
the_end_path  = os.getenv("the_end_path")



# .jar関連の処理

class server_process:
    
    def __init__(self, f_name, maxMemory,minMemory):
        self.server = None
        self.command = ["java", "-server",f'-Xms{minMemory}', f'-Xmx{maxMemory}', "-jar", f_name, "nogui","chcp 65001"]

    def start(self):
        self.server = subprocess.Popen(self.command, stdin=subprocess.PIPE)

    def stop(self):
        input_string = "stop"
        self.server.communicate(input_string.encode())

server = server_process(f_name, maxMemory, minMemory)



# 起動時の処理

@bot.event
async def on_ready():
    print("Botは正常に起動しました")
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('---------------------------')

# サーバーの起動回数を記憶させておく処理（二重起動やコマンドミスによるサーバーファイルの損傷を防げる）

    global count
    count = 0
    global reloadcount
    reloadcount = 0
    


# コマンドの同期

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドの同期を完了")
    except Exception as e:
        print(e)



# サーバー起動

@bot.tree.command(name="mcstart", description="Minecraftサーバーを起動します。（約1分で起動します。）")
async def mcstart(interaction:discord.Interaction):
         global count
         global reloadcount
         global start_time

         count += 1
         reloadcount = 0

         if count == 1:
          server.start() # サーバーを起動
          plugincount = len(glob.glob1(plugin,"*.jar"))

          embed = discord.Embed(
                          title="サーバーを起動中...",
                          color=0xb5f1ff,
                          )
          embed.add_field(name="現在のバージョン",value=f"```{f_name}```")
          embed.add_field(name="導入されているプラグイン数",value=f"```{plugincount}個```")
          start_time = time.time()

          return await interaction.response.send_message(embed=embed)




         else:
             count > 1
             embed = discord.Embed(
                          title="サーバーエラー",
                          color=0xf70707,
                          )
             embed.add_field(name="`403 Forbidden`",value="サーバーが既に起動中またはサーバー読み込み中の場合、起動コマンドは使用できません。",inline=False)
             embed.set_footer(text="\N{No Entry}サーバーの操作が正常にできない場合は、管理者へお問い合わせください。")

             await interaction.response.send_message(embed=embed)



#　サーバー停止

@bot.tree.command(name="mcstop", description="Minecraftサーバーを停止します。（※間違えてサーバーを起動して停止させたい場合、サーバーの起動完了後にコマンドを使用してください。）")
async def mcstop(interaction:discord.Interaction):
          global count
          global reloadcount

          if count > 0:

           # ファイルの更新日時を取得

           warld_time = os.path.getmtime(world_path)
           nether_time = os.path.getmtime(nether_path)
           the_end_time = os.path.getmtime(the_end_path)
            
           elapsed_time = int(time.time() - start_time)
           elapsed_hour = elapsed_time // 3600
           elapsed_minute = (elapsed_time % 3600) // 60
           elapsed_second = (elapsed_time % 3600 % 60)

           embed = discord.Embed(
                          title="サーバーを停止中...",
                          color=0xd8b5ff,
                          )
           embed.add_field(name="サーバー起動時間",value=str(elapsed_hour).zfill(0) +"時間" + str(elapsed_minute).zfill(2) + "分" + str(elapsed_second).zfill(2) +"秒",inline=False)
           embed.add_field(name="停止まで",value="```1分```",inline=False)
           embed.add_field(name="ワールドデータ最終更新日時",value=f"```{time.ctime(warld_time)}```",inline=False)
           embed.add_field(name="ネザーデータ最終更新日時",value=f"```{time.ctime(nether_time)}```",inline=False)
           embed.add_field(name="エンドデータ最終更新日時",value=f"```{time.ctime(the_end_time)}```",inline=False)

           await interaction.response.send_message(embed=embed)

           # サーバー読み込み中の停止を防ぐため、60秒待機
           time.sleep(60) 

           # サーバーを停止
           server.stop()  

           count = 0
           reloadcount = 0

          else:
           embed = discord.Embed(
                          title="サーバーエラー",
                          color=0xf70707,
                          )
           embed.add_field(name="`403 Forbidden`",value="サーバーは現在停止しています。\n「/mcstart」コマンドでサーバーを起動してください。",inline=False)
           
           await interaction.response.send_message(embed=embed)



#　サーバー再起動

@bot.tree.command(name="mcreload", description="Minecraftサーバーを再起動します。（約2分で再起動します。このコマンドは通常は使用しないでください。）")
async def mcreload(interaction:discord.Interaction):
          global count
          global reloadcount

          reloadcount += 1

          if count > 0:

           embed = discord.Embed(
                          title="サーバーを再起動します...",
                          color=0x0000ff,
                          )
           embed.add_field(name="再起動回数",value=f"`{reloadcount}回`")
           embed.add_field(name="再起動完了まで",value="`約2分`")

           await interaction.response.send_message(embed=embed)

           # サーバー読み込み中のリロードを防ぐため、60秒待機
           time.sleep(60) 

           # サーバー停止
           server.stop()

           # 完全に停止する前にコマンドが反映されることを防ぐため、サーバーが停止してから10秒待機
           time.sleep(10) 
           
           # サーバー起動
           server.start()
           count = 1

          else:
           reloadcount = 0
           embed = discord.Embed(
                          title="サーバーエラー",
                          color=0xf70707,
                          )
           embed.add_field(name="`403 Forbidden`",value="サーバーは現在起動していません。",inline=False)
           embed.set_footer(text="\N{No Entry}サーバーの操作が正常にできない場合は、管理者へお問い合わせください。")
           
           await interaction.response.send_message(embed=embed)



# サーバー情報取得
@bot.tree.command(name="serverip", description="Minecraftサーバー接続に必要なIPアドレス情報を表示します。")
async def serverip(interaction:discord.Interaction):

           embed = discord.Embed(
                          title="Minecraftサーバーアドレス情報",
                          color=0xff00ff,
                          )
           embed.add_field(name="サーバーアドレス",value=f"```{global_ip}```")
           embed.add_field(name="ポート（Java）",value=f"```{port_java}```")
           embed.add_field(name="ポート（統合版）",value=f"```{port_be}```")
           embed.add_field(name="LiveKit専用ポート",value=f"```{port_livekit}```")
           embed.add_field(name="BlueMap専用ポート",value=f"```{port_bluemap}```")
           embed.set_footer(text="※JavaEditionの場合、（「サーバーアドレス」:「ポート」）の形式で入力")

           await interaction.response.send_message(embed=embed)
        


bot.run(os.environ["TOKEN"])
