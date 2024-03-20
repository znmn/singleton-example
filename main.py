"""
Contoh penggunaan Creational Pattern (Singleton)
Singleton digunakan untuk membuat sebuah class yang hanya bisa memiliki satu instance saja.
Ini biasa digunakan untuk membuat koneksi ke database, logging, caching, dll (Untuk integritas data, dan penggunaan memory yang optimal).
Untuk case kali ini saya menggunakan singleton pattern untuk membuat class Database (json) yang hanya bisa memiliki satu instance saja.
"""


import json
import os
import uuid
from typing import Union


class PersonDB:
    __instance = None

    def __new__(cls, json_file: str):
        # Cek apakah instance belum pernah di instansiasi
        if not cls.__instance:
            # Cek apakah file json ada
            if not os.path.exists(json_file):
                raise FileNotFoundError(f'{json_file} not found')

            # Jika belum pernah di instansiasi, maka buat instance baru
            cls.__instance = super().__new__(cls)
            cls.__instance._json_file = json_file

            with open(json_file, 'r') as file:
                cls.__instance.__data = json.load(file)

        # Return instance yang sudah pernah di instansiasi sebelumnya
        return cls.__instance

    # Method untuk membuat/menambah data baru
    def create(self, record: dict) -> dict:
        # Menggunakan UUID v4 untuk membuat id
        record['id'] = str(uuid.uuid4())
        self.__data.append(record)
        self.__save()
        return record

    # Method untuk mengambil semua data
    def reads(self) -> list:
        return self.__data

    # Method untuk mengambil data berdasarkan id
    def read(self, id: str) -> Union[dict, str]:
        filtered = self.__filter_data_by_id(id)
        return filtered[0] if filtered else f'No Data with id {id}'

    # Method untuk mengupdate data berdasarkan id
    def update(self, id: str, record: dict) -> Union[dict, str]:
        filtered = self.__filter_data_by_id(id)
        if filtered:
            filtered[0].update(record)
            self.__save()
            return filtered[0]
        return f'No Data with id {id}'

    # Method untuk menghapus data berdasarkan id
    def delete(self, id: str) -> str:
        filtered = self.__filter_data_by_id(id)
        if filtered:
            self.__data.remove(filtered[0])
            self.__save()
            return f'Deleted Data with id {id}'
        return f'No Data with id {id}'

    # Private method untuk filter data berdasarkan id
    def __filter_data_by_id(self, id: str) -> list:
        return [record for record in self.__data if record['id'] == id]

    # Private method untuk menyimpan data ke file json
    def __save(self) -> None:
        with open(self._json_file, 'w') as file:
            json.dump(self.__data, file, indent=4)


if __name__ == '__main__':
    db1 = PersonDB("data.json")
    db2 = PersonDB("data2.json")

    # True karena db1 dan db2 adalah instance yang sama
    print(f"Apakah db1 dan db2 instance yang sama: {db1 is db2}\n")

    # Instance db2 Menampilkan data dari file data.json bukan dari file data2.json karena instance tersebut sudah pernah di instansiasi sebelumnya
    print("Data db1: \n", db1.reads())
    print("Data db2: \n", db2.reads())
