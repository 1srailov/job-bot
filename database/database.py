import sqlite3, os, glob


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database/job.db')

    async def add_job(self, city, message, photo):
        await self.delete_limit_job(city)
        await self.__write(f"INSERT INTO jobs (city, message, image) VALUES ('{city}', '{message}', '{photo}')")

    async def delete_job(self, message):
        id = await self.get_image_id_by_message(message)
        files = glob.glob(f'image/{id[0][0]}')
        os.remove(files[0])

        # await os.remove(glob.glob(f'file .jpg'))
        await self.__write(f"delete from jobs where message = '{message}'")


    async def delete_limit_job(self, city):
        count = await self.__read(f"select count(id), id from jobs where city = '{city}'")
        if count[0][0] >= 100:
            id = await self.get_image_id_by_id(count[0][1])
            files = glob.glob(f'image/{id[0][0]}')
            os.remove(files[0])
            await self.__read(f"delete from jobs where id in (select min(id) from jobs where city = '{city}')")
    
    async def get_job(self, city):
        return await self.__read(f"SELECT * FROM jobs WHERE city = '{city}' ORDER BY id DESC")

    async def get_image_id_by_message(self, message):
        return await self.__read(f"SELECT image FROM jobs WHERE message = '{message}'")

    async def get_image_id_by_id(self, id):
        return await self.__read(f"SELECT image FROM jobs WHERE id = {id}")

    async def get_count(self, city):
        return await self.__read(f"select count(id) from jobs where city = '{city}'")
 


    async def __read(self, query):
        c = self.connection.cursor()
        c.execute(query)

        return c.fetchall()

    async def __write(self, query):
        c = self.connection.cursor()
        c.execute(query)

        c.close()
        self.connection.commit()
