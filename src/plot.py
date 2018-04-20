from nightModels import Post, Weibo, Thread, use
from nlp import is_possitive
from utils import removeAll

import datetime
import json
import time

def slice_array(start, end, project, step=1):
    start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")
    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
    array = get_data(start, end, project)
    array.sort(key=lambda x: x.post_date)

    data = []
    holder = []
    xaxis = []

    timestep = datetime.timedelta(minutes=step)

    index = 0
    for mark in gen(start, end, timestep):
        xaxis.append(mark)
        holder = []
        while True and index < len(array):
            cursor = array[index]
            if cursor.post_date - mark < timestep:
                holder.append(cursor)
                index += 1
            else:
                break
        data.append(holder)
    return {"xaxis": xaxis, "data": data}


def gen(start, end, timestep):
    cursor = start
    while cursor < end:
        yield cursor
        cursor += timestep

def get_data(start, end, project):
    db = use(project)
    with Post.bind_ctx(db), Weibo.bind_ctx(db), Thread.bind_ctx(db):
        return list(
            Post.select().where(Post.post_date >= start, Post.post_date < end)
        ) + list(
            Weibo.select().where(Weibo.post_date >= start, Weibo.post_date < end)
        ) + list(
            Thread.select().where(Thread.post_date >= start, Thread.post_date < end)
        )

def plot_pos(start, end, project, step=1):
    data = slice_array(start, end, project, step)
    pos_data = []
    for stepdata in data['data']:
        total = len(stepdata)
        if not total:
            pos_data.append(0.5)

        pos_count = 0
        for item in stepdata:
            content = removeAll(item.content)
            if not content:
                total -= 1
                continue
            if is_possitive(content):
                pos_count += 1

        if not pos_count:
            pos_data.append(0.5)
        else:
            pos_data.append(float(pos_count)/total)
    xaxis = [item.strftime("%Y-%m-%d %H:%M") for item in data['xaxis']]
    return {'data': pos_data, 'xaxis': xaxis}

