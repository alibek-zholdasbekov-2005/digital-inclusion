import { api } from './client'
import type { ForumPost, ForumTopic } from '../types'

type Paginated<T> = { results?: T[] } | T[]

function unwrap<T>(data: Paginated<T>): T[] {
  if (Array.isArray(data)) return data
  return data.results ?? []
}

export async function listTopics(search?: string) {
  const { data } = await api.get('/api/forum/topics/', {
    params: search ? { search } : undefined,
  })
  return unwrap<ForumTopic>(data)
}

export async function getTopic(id: number | string) {
  const { data } = await api.get(`/api/forum/topics/${id}/`)
  return data as ForumTopic
}

export async function createTopic(title: string) {
  const { data } = await api.post('/api/forum/topics/', { title })
  return data as ForumTopic
}

export async function listPosts(topicId: number | string) {
  const { data } = await api.get('/api/forum/posts/', {
    params: { topic: topicId },
  })
  return unwrap<ForumPost>(data)
}

export async function createPost(
  topicId: number,
  text: string,
  image?: File | null,
) {
  if (image) {
    const fd = new FormData()
    fd.append('topic', String(topicId))
    fd.append('text', text)
    fd.append('image', image)
    const { data } = await api.post('/api/forum/posts/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data as ForumPost
  }
  const { data } = await api.post('/api/forum/posts/', {
    topic: topicId,
    text,
  })
  return data as ForumPost
}
