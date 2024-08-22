import React, { useEffect, useState } from 'react'
import axios from 'axios'
import styles from '../styles/MovieCollections.module.scss'

interface Movie {
  title: string
  poster: string
  background: string
}

interface MovieCollection {
  title: string
  poster: string
  background: string
  movies: Movie[]
}

interface MovieCollectionsProps {
  urlCollections: string
}

const MovieCollections: React.FC<MovieCollectionsProps> = ({
  urlCollections
}) => {
  const [collections, setCollections] = useState<MovieCollection[]>([])

  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const response = await axios.get(urlCollections)
        setCollections(response.data)
      } catch (error) {
        console.error('Error fetching movie collections:', error)
      }
    }

    fetchCollections().then((r) => r)
  }, [urlCollections])

  return (
    <div className="space-y-8">
      {collections.map((collection, index) => (
        <div key={index} className={styles.collection}>
          <h2 className="mb-4 text-xl font-bold">{collection.title}</h2>
          <div>
            <img
              key={0}
              src={collection.poster}
              alt={collection.title}
              className="m-1.5 inline-block h-60 rounded-lg shadow-lg shadow-zinc-700"
            />
            {collection.movies.map((movie, idx) => (
              <img
                key={idx + 1}
                src={movie.poster}
                alt={movie.title}
                className="m-2 inline-block h-60 rounded-lg shadow-lg shadow-zinc-700"
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

export default MovieCollections
