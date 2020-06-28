import express from 'express'
import helmet from 'helmet'
import morgan from 'morgan'

const app: express.Application = express()
const port: number = 3000

app.use(helmet())
app.use(express.json())
app.use(morgan('common'))

app.get('/', (req, res) => {
  res.json({ body: 'Hello World!' })
})

app.use((err:any, req:any, res:any, next:any) => {
  // eslint-disable-next-line no-console
  console.error(err.stack)
  res.status(500).send('Something went wrong!')
})

// eslint-disable-next-line no-console
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
